"""
Configuration settings for Tavily Register.

This module contains all configuration constants and settings used throughout
the application. It supports environment variables for flexible configuration.
"""
import os
from typing import Union


def get_env_bool(key: str, default: bool = False) -> bool:
    """Get boolean value from environment variable."""
    value = os.getenv(key, str(default)).lower()
    return value in ('true', '1', 'yes', 'on')


def get_env_int(key: str, default: int) -> int:
    """Get integer value from environment variable."""
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default


def get_env_str(key: str, default: str) -> str:
    """Get string value from environment variable."""
    return os.getenv(key, default)


# Tavily related configuration
TAVILY_HOME_URL = get_env_str("TAVILY_HOME_URL", "https://app.tavily.com/home")
TAVILY_SIGNUP_URL = get_env_str(
    "TAVILY_SIGNUP_URL", "https://app.tavily.com/home")

# Email configuration
EMAIL_DOMAIN = get_env_str("EMAIL_DOMAIN", "2925.com")
# Replace with your email prefix
EMAIL_PREFIX = get_env_str("EMAIL_PREFIX", "user123")
MAIN_EMAIL = f"{EMAIL_PREFIX}@{EMAIL_DOMAIN}"

# 2925.com email access configuration
EMAIL_CHECK_URL = get_env_str("EMAIL_CHECK_URL", "https://2925.com")

# Registration configuration
DEFAULT_PASSWORD = get_env_str("DEFAULT_PASSWORD", "TavilyAuto123!")

# File paths
API_KEYS_FILE = get_env_str("API_KEYS_FILE", "api_keys.md")
COOKIES_FILE = get_env_str("COOKIES_FILE", "email_cookies.json")

# Wait time configuration (seconds)
WAIT_TIME_SHORT = get_env_int("WAIT_TIME_SHORT", 2)
WAIT_TIME_MEDIUM = get_env_int("WAIT_TIME_MEDIUM", 5)
WAIT_TIME_LONG = get_env_int("WAIT_TIME_LONG", 10)
EMAIL_CHECK_INTERVAL = get_env_int("EMAIL_CHECK_INTERVAL", 30)
MAX_EMAIL_WAIT_TIME = get_env_int("MAX_EMAIL_WAIT_TIME", 300)  # 5 minutes

# Browser configuration
HEADLESS = get_env_bool("HEADLESS", False)  # Set to True for headless mode
BROWSER_TIMEOUT = get_env_int("BROWSER_TIMEOUT", 30000)  # 30 seconds
# Options: "chromium", "firefox", "webkit"
BROWSER_TYPE = get_env_str("BROWSER_TYPE", "firefox")

# Logging configuration
LOG_LEVEL = get_env_str("LOG_LEVEL", "INFO")
DEBUG_MODE = get_env_bool("DEBUG_MODE", False)

# Development settings
ENABLE_SCREENSHOTS = get_env_bool("ENABLE_SCREENSHOTS", True)
SAVE_HTML_LOGS = get_env_bool("SAVE_HTML_LOGS", True)
