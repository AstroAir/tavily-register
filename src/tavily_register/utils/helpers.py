"""
Utility functions and helpers for Tavily Register.

This module contains common utility functions used throughout the application
including email generation, file operations, and browser helpers.
"""
import random
import string
import time
import json
from datetime import datetime
from typing import Optional, Any, List, Dict
from ..config.settings import EMAIL_PREFIX, EMAIL_DOMAIN, API_KEYS_FILE


def generate_random_suffix(length: int = 8) -> str:
    """
    Generate a random string suffix of specified length.

    Args:
        length (int): The length of the random suffix. Default is 8.

    Returns:
        str: A random string consisting of lowercase letters and digits.
    """
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_email(email_prefix: Optional[str] = None) -> str:
    """
    Generate a random email address using a prefix and a random suffix.

    Args:
        email_prefix (Optional[str]): The prefix to use for the email address.
            If None, uses the default prefix from config.

    Returns:
        str: A generated email address in the format prefix-suffix@domain.
    """
    # Use dynamic prefix + random suffix
    if email_prefix is None:
        prefix = EMAIL_PREFIX  # Use default prefix from config
    else:
        prefix = email_prefix

    suffix = generate_random_suffix()
    return f"{prefix}-{suffix}@{EMAIL_DOMAIN}"


def generate_password() -> str:
    """
    Generate a secure password.

    Returns:
        str: The default password from config.
    """
    from ..config.settings import DEFAULT_PASSWORD
    return DEFAULT_PASSWORD


def save_api_key(email: str, api_key: str, password: Optional[str] = None) -> None:
    """
    Save API key and account information to a file in a simplified format.

    Args:
        email (str): The email address associated with the API key.
        api_key (str): The API key to save.
        password (Optional[str]): The password for the account, if available.

    Returns:
        None
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Simplified format: email,password,API Key,registration time;
    account_line = f"{email},{password if password else 'N/A'},{api_key},{timestamp};\n"

    # Append to end of file
    try:
        with open(API_KEYS_FILE, 'a', encoding='utf-8') as f:
            f.write(account_line)
    except FileNotFoundError:
        # If file doesn't exist, create new file
        with open(API_KEYS_FILE, 'w', encoding='utf-8') as f:
            f.write(account_line)

    print(f"✅ Account information saved to {API_KEYS_FILE}")
    print(f"📧 Email: {email}")
    print(f"🔐 Password: {password if password else 'N/A'}")
    print(f"🔑 API Key: {api_key}")
    print(f"⏰ Time: {timestamp}")


def save_cookies(cookies: List[Dict[str, Any]], filename: str) -> None:
    """
    Save cookies to a file in JSON format.

    Args:
        cookies (List[Dict[str, Any]]): The list of cookies to save.
        filename (str): The file path where cookies will be saved.

    Returns:
        None
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(cookies, f, indent=2)


def load_cookies(filename: str) -> Optional[Any]:
    """
    Load cookies from a file.

    Args:
        filename (str): The file path from which to load cookies.

    Returns:
        Optional[Any]: The loaded cookies if the file exists, otherwise None.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def wait_with_message(seconds: float, message: str = "Waiting") -> None:
    """
    Wait for a specified number of seconds, displaying a message.

    Args:
        seconds (float): The number of seconds to wait.
        message (str): The message to display while waiting.

    Returns:
        None
    """
    print(f"⏳ {message}, waiting {seconds} seconds...")
    time.sleep(seconds)


def take_screenshot(page: Any, filename: Optional[str] = None) -> Optional[str]:
    """
    Take a screenshot of the current browser page.

    Args:
        page (Any): The browser page object supporting the screenshot method.
        filename (Optional[str]): The filename to save the screenshot as.
            If None, a filename is generated using the current timestamp.

    Returns:
        Optional[str]: The filename if the screenshot was saved successfully, otherwise None.
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"

    try:
        page.screenshot(path=filename)
        print(f"📸 Screenshot saved: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Failed to take screenshot: {e}")
        return None


def log_action(action: str, details: Optional[str] = None) -> None:
    """
    Log an action with a timestamp.

    Args:
        action (str): The action description.
        details (Optional[str]): Additional details about the action.

    Returns:
        None
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"[{timestamp}] {action}"
    if details:
        message += f" - {details}"
    print(message)
