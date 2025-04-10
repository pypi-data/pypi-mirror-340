"""
LocatAI package setup file.

This script configures the package for distribution via PyPI.
"""

from setuptools import setup, find_packages
import os

# Read version from __init__.py
with open(os.path.join("locatai", "__init__.py"), "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"\'')
            break

# Read README.md for long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Repository URL - ensure it's consistent across all metadata
repo_url = "https://github.com/Divyarajsinh-Dodia/locatai"

setup(
    name="locatai",
    version=version,
    description="AI-powered element locator for Selenium WebDriver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="LocatAI Team",
    author_email="divyarajsinh.dodia@outlook.com",
    url=repo_url,
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "locatai": ["ai/prompts/*.txt", "config/*.json"],  # Updated to locatai
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="selenium, testing, automation, ai, openai, test-automation, webdriver, locator, element-finding",
    install_requires=[
        "selenium>=4.0.0",
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
    ],
    python_requires=">=3.8",
    project_urls={
        "Bug Reports": f"{repo_url}/issues",
        "Source": repo_url,
        "Documentation": f"{repo_url}/blob/main/README.md",
    },
)