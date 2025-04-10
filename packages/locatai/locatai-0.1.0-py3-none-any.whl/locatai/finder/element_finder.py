"""
AI-powered element finder for Selenium WebDriver.
"""

import hashlib
import json
import os
import time
import atexit
import re
from collections import OrderedDict
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

from locatai.ai.providers.openai_provider import GetElementUsingAI
from locatai.utils.analytics import AIUsageTracker

# Configure logging
logger = logging.getLogger(__name__)

class ElementFinder:
    # LRU Cache for storing previously found locators
    _locator_cache = OrderedDict()
    _locator_success = {}  # Track success/failure stats for each locator
    _element_load_times = {}  # Track element load times for smart timeouts
    _cache_max_size = 100
    _cache_expiry_seconds = 3600  # 1 hour
    _cache_file = "locator_cache.json"
    _default_timeout = 10
    _performance_threshold = 1.5  # Load time multiplier before adjusting

    @staticmethod
    def _get_smart_timeout(element_description, url):
        """Dynamically calculate timeout based on historical performance"""
        key = f"{url}::{element_description}"
        if key in ElementFinder._element_load_times:
            # Use historical data with a buffer
            avg_time = ElementFinder._element_load_times[key]["avg"]
            return min(30, max(3, avg_time * ElementFinder._performance_threshold))
        return ElementFinder._default_timeout

    @staticmethod
    def _update_load_time_stats(element_description, url, load_time):
        """Track and update element load times"""
        key = f"{url}::{element_description}"
        if key not in ElementFinder._element_load_times:
            ElementFinder._element_load_times[key] = {"count": 0, "total": 0, "avg": ElementFinder._default_timeout}

        stats = ElementFinder._element_load_times[key]
        stats["count"] += 1
        stats["total"] += load_time
        stats["avg"] = stats["total"] / stats["count"]

    @staticmethod
    def _clean_dom_for_ai(dom):
        """Strip sensitive data and reduce DOM size before sending to AI"""
        # Remove common patterns for sensitive data
        cleaned = re.sub(r'(password|token|key|secret|auth)\s*=\s*["\'](.*?)["\']', r'\1="[REDACTED]"', dom, flags=re.IGNORECASE)

        # Remove script contents (often large and unnecessary)
        cleaned = re.sub(r'<script\b[^<]*(?:(?!</script>)<[^<]*)*</script>', '<script>[REMOVED]</script>', cleaned)

        # Keep the structural HTML but remove large text nodes
        cleaned = re.sub(r'>([^<]{1000,})<', '>[TEXT_TRUNCATED]<', cleaned)

        return cleaned

    @staticmethod
    def _get_dom_fingerprint(dom):
        """Generate a short fingerprint of DOM to detect changes"""
        # Use a substring of DOM for efficiency (header + some body)
        sample_size = min(len(dom), 5000)  # First 5KB is often enough
        return hashlib.md5(dom[:sample_size].encode('utf-8')).hexdigest()[:10]

    @staticmethod
    def _update_locator_success(cache_key, success=True):
        """Track success/failure rates for locators"""
        if cache_key not in ElementFinder._locator_success:
            ElementFinder._locator_success[cache_key] = {"success": 0, "failure": 0, "attempts": 0}

        stats = ElementFinder._locator_success[cache_key]

        if success:
            stats["success"] += 1
        else:
            stats["failure"] += 1

        stats["attempts"] += 1

        # Calculate success rate
        success_rate = stats["success"] / stats["attempts"]

        # If too many failures or success rate too low, remove from cache
        if (stats["attempts"] >= 5 and success_rate < 0.6) or stats["failure"] >= 3:
            logger.info(f"Removing unreliable locator from cache: {cache_key}")
            ElementFinder._locator_cache.pop(cache_key, None)
            return False

        return True

    @staticmethod
    def _analyze_element_failure(driver, by, selector, error):
        """Provides detailed diagnostics for element location failures"""
        reason = "Unknown failure"

        try:
            # Check if element exists but is not visible/enabled
            elements = driver.find_elements(by, selector)

            if not elements:
                reason = "Element does not exist in DOM"
            else:
                # Element exists but might not be visible/clickable
                element = elements[0]
                if not element.is_displayed():
                    reason = "Element exists but is not displayed"
                elif not element.is_enabled():
                    reason = "Element exists but is not enabled"
                else:
                    # Check if element is outside viewport
                    script = """
                        var elem = arguments[0];
                        var rect = elem.getBoundingClientRect();
                        return {
                            visibleInViewport: (
                                rect.top >= 0 &&
                                rect.left >= 0 &&
                                rect.bottom <= window.innerHeight &&
                                rect.right <= window.innerWidth
                            ),
                            position: {
                                top: rect.top,
                                left: rect.left,
                                bottom: rect.bottom,
                                right: rect.right
                            },
                            viewport: {
                                height: window.innerHeight,
                                width: window.innerWidth
                            }
                        };
                    """
                    result = driver.execute_script(script, element)
                    if not result['visibleInViewport']:
                        reason = f"Element outside viewport: {result['position']}"
        except:
            pass

        return f"Element failure: {reason}. Original error: {str(error)}"

    @staticmethod
    def _cleanup_cache():
        """Remove expired entries from cache"""
        current_time = time.time()
        expired_keys = []

        for key, (locator, timestamp) in list(ElementFinder._locator_cache.items()):
            if current_time - timestamp > ElementFinder._cache_expiry_seconds:
                expired_keys.append(key)

        for key in expired_keys:
            logger.info(f"Removing expired cache key: {key}")
            ElementFinder._locator_cache.pop(key, None)

        # If cache is still too big after removing expired items, remove oldest items
        while len(ElementFinder._locator_cache) > ElementFinder._cache_max_size:
            expired = ElementFinder._locator_cache.popitem(last=False)  # Remove oldest item
            logger.info(f"Cache size exceeded. Removed oldest entry: {expired[0]}")

        logger.debug(f"Cache cleanup completed. Current size: {len(ElementFinder._locator_cache)}")

    @staticmethod
    def load_cache():
        """Load the locator cache from disk if available"""
        try:
            if os.path.exists(ElementFinder._cache_file):
                with open(ElementFinder._cache_file, 'r') as f:
                    loaded_data = json.load(f)

                    # Convert stored data back to proper format
                    for key, value in loaded_data.items():
                        by_name, selector, timestamp = value
                        # Convert string representation to actual By constant
                        by_constant = getattr(By, by_name)
                        ElementFinder._locator_cache[key] = ((by_constant, selector), timestamp)

                logger.info(f"Loaded {len(ElementFinder._locator_cache)} cached locators from file")

                # Also load success stats if available
                stats_file = ElementFinder._cache_file.replace('.json', '_stats.json')
                if os.path.exists(stats_file):
                    with open(stats_file, 'r') as f:
                        ElementFinder._locator_success = json.load(f)

                # Load element timing data if available
                timing_file = ElementFinder._cache_file.replace('.json', '_timing.json')
                if os.path.exists(timing_file):
                    with open(timing_file, 'r') as f:
                        ElementFinder._element_load_times = json.load(f)
        except Exception as e:
            logger.error(f"Error loading cache from file: {str(e)}")
            # If loading fails, start with empty cache
            ElementFinder._locator_cache = OrderedDict()

    @staticmethod
    def save_cache():
        """Save the current cache to disk"""
        try:
            # Convert cache to serializable format
            serializable_cache = {}
            for key, ((by_obj, selector), timestamp) in ElementFinder._locator_cache.items():
                # Store By constant as string name
                by_name = next(name for name in dir(By) if getattr(By, name) == by_obj)
                serializable_cache[key] = (by_name, selector, timestamp)

            with open(ElementFinder._cache_file, 'w') as f:
                json.dump(serializable_cache, f)

            # Also save success stats
            stats_file = ElementFinder._cache_file.replace('.json', '_stats.json')
            with open(stats_file, 'w') as f:
                json.dump(ElementFinder._locator_success, f)

            # Save element timing data
            timing_file = ElementFinder._cache_file.replace('.json', '_timing.json')
            with open(timing_file, 'w') as f:
                json.dump(ElementFinder._element_load_times, f)

            logger.info(f"Saved {len(ElementFinder._locator_cache)} cached locators to file")
        except Exception as e:
            logger.error(f"Error saving cache to file: {str(e)}")

    @staticmethod
    def FindElementByAI(driver, elementDescription, timeout=None, retry_attempts=2):
        """
        Finds a web element using AI-generated locators based on element description.
        Implements error recovery with retries and success tracking.

        Args:
            driver: Selenium WebDriver instance
            elementDescription: Text description of the element to find
            timeout: Maximum time (seconds) to wait for element to be present
            retry_attempts: Number of additional attempts if initial lookup fails

        Returns:
            WebElement: The found Selenium WebElement

        Raises:
            NoSuchElementException: If element cannot be found
        """
        tracker = AIUsageTracker.get_instance()
        start_time = time.time()

        try:
            # Use smart timeout if none specified
            if timeout is None:
                timeout = ElementFinder._get_smart_timeout(elementDescription, driver.current_url)

            # Clean up expired cache entries periodically
            ElementFinder._cleanup_cache()

            # Get DOM fingerprint for cache invalidation
            dom = driver.page_source
            dom_fingerprint = ElementFinder._get_dom_fingerprint(dom)
            current_time = time.time()

            # Include fingerprint in cache key
            cache_key = f"{driver.current_url}::{elementDescription}::{dom_fingerprint}"

            # Try the cache first
            if cache_key in ElementFinder._locator_cache:
                logger.info(f"Using cached locator for '{elementDescription}'")
                tracker.increment_cache_access(hit=True)

                try:
                    (by, selector_value), _ = ElementFinder._locator_cache[cache_key]
                    element = WebDriverWait(driver, timeout).until(
                        EC.element_to_be_clickable((by, selector_value))
                    )
                    # Move to end (mark as recently used)
                    ElementFinder._locator_cache.move_to_end(cache_key)
                    # Update timestamp
                    ElementFinder._locator_cache[cache_key] = ((by, selector_value), current_time)
                    # Record success
                    ElementFinder._update_locator_success(cache_key, True)
                    tracker.increment_element_result(success=True)

                    # Record load time for future optimization
                    load_time = time.time() - start_time
                    ElementFinder._update_load_time_stats(elementDescription, driver.current_url, load_time)

                    return element

                except (NoSuchElementException, StaleElementReferenceException) as e:
                    # Record failure with detailed analysis
                    error_details = ElementFinder._analyze_element_failure(driver, by, selector_value, e)
                    logger.warning(f"Cached locator failed: {error_details}")

                    ElementFinder._update_locator_success(cache_key, False)
                    tracker.increment_element_result(success=False)
                    # Cache entry failed, will try fresh lookup
            else:
                tracker.increment_cache_access(hit=False)

            # Fresh lookup with retries
            clean_dom = ElementFinder._clean_dom_for_ai(dom)

            for attempt in range(retry_attempts + 1):
                try:
                    tracker.increment_api_call()
                    ele = GetElementUsingAI(clean_dom, elementDescription)

                    if ele == "Element Not Found":
                        tracker.increment_element_result(success=False)
                        raise NoSuchElementException(f"AI could not identify element: {elementDescription}")

                    if ':' in ele:
                        parts = ele.split(':', 1)
                        selector_type = parts[0].strip().upper()
                        selector_value = parts[1].strip()

                        by = ElementFinder.verify_and_convert_locator(selector_type, selector_value)

                        # Wait for element to be clickable with timeout
                        element = WebDriverWait(driver, timeout).until(
                            EC.element_to_be_clickable(by)
                        )

                        # Cache the successful locator with timestamp
                        ElementFinder._locator_cache[cache_key] = (by, current_time)

                        # Keep cache size in check
                        if len(ElementFinder._locator_cache) > ElementFinder._cache_max_size:
                            ElementFinder._locator_cache.popitem(last=False)  # Remove oldest item

                        # Record success and update stats
                        load_time = time.time() - start_time
                        ElementFinder._update_load_time_stats(elementDescription, driver.current_url, load_time)
                        tracker.increment_element_result(success=True)

                        return element
                    else:
                        raise ValueError(f"Invalid selector format: {ele}")

                except Exception as e:
                    if attempt < retry_attempts:
                        error_details = ElementFinder._analyze_element_failure(
                            driver, by, selector_value, e) if 'by' in locals() else str(e)
                        logger.warning(f"Attempt {attempt+1} failed: {error_details}. Retrying...")
                        time.sleep(1)  # Short delay before retry
                    else:
                        # Final attempt failed
                        tracker.increment_element_result(success=False)
                        logger.error(f"All {retry_attempts+1} attempts failed for '{elementDescription}'")
                        raise

        except Exception as e:
            logger.error(f"Error finding element '{elementDescription}': {str(e)}")
            raise

    @staticmethod
    def FindElementsByAI(driver, elementDescription, timeout=None):
        """
        Finds multiple web elements using AI-generated locators based on description.

        Args:
            driver: Selenium WebDriver instance
            elementDescription: Text description of elements to find
            timeout: Maximum time (seconds) to wait for elements

        Returns:
            list: List of WebElements matching the description
        """
        tracker = AIUsageTracker.get_instance()
        start_time = time.time()

        try:
            # Use smart timeout if none specified
            if timeout is None:
                timeout = ElementFinder._get_smart_timeout(elementDescription, driver.current_url)

            # Clean up expired cache entries periodically
            ElementFinder._cleanup_cache()

            dom = driver.page_source
            dom_fingerprint = ElementFinder._get_dom_fingerprint(dom)
            current_time = time.time()

            # Check cache first to avoid redundant API calls
            cache_key = f"{driver.current_url}::multiple::{elementDescription}::{dom_fingerprint}"

            if cache_key in ElementFinder._locator_cache:
                logger.info(f"Using cached locator for multiple '{elementDescription}'")
                tracker.increment_cache_access(hit=True)

                try:
                    (by, selector_value), _ = ElementFinder._locator_cache[cache_key]
                    # Move to end (mark as recently used)
                    ElementFinder._locator_cache.move_to_end(cache_key)
                    # Update timestamp
                    ElementFinder._locator_cache[cache_key] = ((by, selector_value), current_time)
                    elements = WebDriverWait(driver, timeout).until(
                        lambda d: d.find_elements(by, selector_value) if len(d.find_elements(by, selector_value)) > 0 else None
                    )
                    # Record success
                    ElementFinder._update_locator_success(cache_key, True)
                    tracker.increment_element_result(success=True)

                    # Record load time for future optimization
                    load_time = time.time() - start_time
                    ElementFinder._update_load_time_stats(f"multiple::{elementDescription}", driver.current_url, load_time)

                    return elements
                except Exception as e:
                    # Record failure
                    error_details = ElementFinder._analyze_element_failure(driver, by, selector_value, e)
                    logger.warning(f"Cached multiple elements locator failed: {error_details}")

                    ElementFinder._update_locator_success(cache_key, False)
                    tracker.increment_element_result(success=False)
                    # Continue to get a fresh locator
            else:
                tracker.increment_cache_access(hit=False)

            # Clean DOM before sending to AI
            clean_dom = ElementFinder._clean_dom_for_ai(dom)

            tracker.increment_api_call()
            ele = GetElementUsingAI(clean_dom, f"All elements that are: {elementDescription}")

            if ele == "Element Not Found":
                logger.warning(f"AI could not identify elements: {elementDescription}")
                tracker.increment_element_result(success=False)
                return []

            if ':' in ele:
                parts = ele.split(':', 1)
                selector_type = parts[0].strip().upper()
                selector_value = parts[1].strip()

                logger.info(f"Multiple Selector Type: {selector_type}, Value: {selector_value}")

                by = ElementFinder.verify_and_convert_locator(selector_type, selector_value)

                # Store in cache for future use with timestamp
                ElementFinder._locator_cache[cache_key] = (by, current_time)

                # Keep cache size in check
                if len(ElementFinder._locator_cache) > ElementFinder._cache_max_size:
                    ElementFinder._locator_cache.popitem(last=False)  # Remove oldest item

                # Wait for at least one element to be present
                try:
                    WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located(by)
                    )

                    # Get all matching elements
                    elements = driver.find_elements(by[0], by[1])

                    # Record success and update stats
                    load_time = time.time() - start_time
                    ElementFinder._update_load_time_stats(f"multiple::{elementDescription}", driver.current_url, load_time)
                    tracker.increment_element_result(success=True)

                    return elements
                except:
                    logger.warning(f"No elements found matching '{elementDescription}'")
                    tracker.increment_element_result(success=False)
                    return []
            else:
                logger.error(f"Invalid selector format: {ele}")
                tracker.increment_element_result(success=False)
                return []

        except Exception as e:
            logger.error(f"Error finding elements '{elementDescription}': {str(e)}")
            tracker.increment_element_result(success=False)
            return []

    @staticmethod
    def verify_and_convert_locator(selector_type, selector_value):
        """Convert string selector type to Selenium By object and value tuple"""
        selector_map = {
            "ID": By.ID,
            "NAME": By.NAME,
            "XPATH": By.XPATH,
            "CSS SELECTOR": By.CSS_SELECTOR,
            "CLASS NAME": By.CLASS_NAME,
            "TAG NAME": By.TAG_NAME,
            "LINK TEXT": By.LINK_TEXT,
            "PARTIAL LINK TEXT": By.PARTIAL_LINK_TEXT
        }

        if selector_type in selector_map:
            return selector_map[selector_type], selector_value
        else:
            logger.error(f"Invalid selector type: {selector_type}")
            raise ValueError(f"Invalid selector type: {selector_type}")

    @staticmethod
    def print_usage_report():
        """Print API usage statistics"""
        report = AIUsageTracker.get_instance().get_report()
        logger.info("=== AI Usage Report ===")
        logger.info(f"API Calls: {report['api_calls']}")
        logger.info(f"Cache Hit Rate: {report['cache_hit_rate']:.1%}")
        logger.info(f"Element Success Rate: {report['element_success_rate']:.1%}")
        logger.info(f"Estimated Cost: ${report['estimated_cost']:.4f}")
        logger.info(f"Runtime: {report['runtime_seconds']:.2f} seconds")
        return report


# Load cache when module is imported
ElementFinder.load_cache()

# Register an atexit handler to save cache when program exits
atexit.register(ElementFinder.save_cache)
atexit.register(ElementFinder.print_usage_report)