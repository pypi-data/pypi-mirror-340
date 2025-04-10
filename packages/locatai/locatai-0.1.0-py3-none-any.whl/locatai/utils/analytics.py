"""
Tracks usage statistics and performance metrics for the AI locator.
"""

import time
import logging

logger = logging.getLogger(__name__)

class AIUsageTracker:
    """Tracks OpenAI API usage and effectiveness"""
    _instance = None

    def __init__(self):
        self.api_calls = 0
        self.api_failures = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.element_successes = 0
        self.element_failures = 0
        self.start_time = time.time()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AIUsageTracker()
        return cls._instance

    def increment_api_call(self, success=True):
        self.api_calls += 1
        if not success:
            self.api_failures += 1

    def increment_cache_access(self, hit=True):
        if hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    def increment_element_result(self, success=True):
        if success:
            self.element_successes += 1
        else:
            self.element_failures += 1

    def get_report(self):
        elapsed = time.time() - self.start_time
        return {
            "api_calls": self.api_calls,
            "api_success_rate": (self.api_calls - self.api_failures) / max(1, self.api_calls),
            "cache_hit_rate": self.cache_hits / max(1, (self.cache_hits + self.cache_misses)),
            "element_success_rate": self.element_successes / max(1, (self.element_successes + self.element_failures)),
            "runtime_seconds": elapsed,
            "estimated_cost": self.api_calls * 0.01  # Assuming $0.01 per API call
        }