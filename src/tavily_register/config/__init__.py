"""
Configuration management for Tavily registration.

This package contains settings, constants, and configuration utilities.
"""

from .settings import *

__all__ = [
    "TAVILY_HOME_URL", "TAVILY_SIGNUP_URL", "EMAIL_DOMAIN", "EMAIL_PREFIX",
    "DEFAULT_PASSWORD", "API_KEYS_FILE", "COOKIES_FILE", "WAIT_TIME_SHORT",
    "WAIT_TIME_MEDIUM", "WAIT_TIME_LONG", "HEADLESS", "BROWSER_TYPE"
]
