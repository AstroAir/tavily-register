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
from functools import lru_cache
from typing import Optional, Any, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from playwright._impl._api_structures import SetCookieParam
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


def save_cookies(cookies: List[Dict[str, Any]], filename: str) -> bool:
    """
    Save cookies to a file in JSON format with enhanced error handling.

    Args:
        cookies (List[Dict[str, Any]]): The list of cookies to save.
        filename (str): The file path where cookies will be saved.

    Returns:
        bool: True if cookies were saved successfully, False otherwise.
    """
    try:
        if not cookies:
            print("⚠️ 没有cookies可保存")
            return False

        # Add metadata for better tracking
        cookie_data = {
            'timestamp': time.time(),
            'count': len(cookies),
            'cookies': cookies
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(cookie_data, f, indent=2, ensure_ascii=False)

        print(f"✅ 成功保存 {len(cookies)} 个cookies到 {filename}")
        return True

    except Exception as e:
        print(f"❌ 保存cookies失败: {e}")
        return False


@lru_cache(maxsize=None)
def load_cookies(filename: str) -> Optional[List[Dict[str, Any]]]:
    """
    Load cookies from a file with validation and expiry checking.

    Args:
        filename (str): The file path from which to load cookies.

    Returns:
        Optional[List[Dict[str, Any]]]: The loaded cookies if valid, otherwise None.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle both old format (direct cookie list) and new format (with metadata)
        if isinstance(data, list):
            # Old format - direct cookie list
            cookies = data
            print(f"📂 加载了 {len(cookies)} 个cookies (旧格式)")
        elif isinstance(data, dict) and 'cookies' in data:
            # New format - with metadata
            cookies = data['cookies']
            timestamp = data.get('timestamp', 0)
            count = data.get('count', len(cookies))

            # Check if cookies are too old (older than 7 days)
            current_time = time.time()
            age_days = (current_time - timestamp) / (24 * 3600)

            print(f"📂 加载了 {count} 个cookies (保存于 {age_days:.1f} 天前)")

            if age_days > 7:
                print("⚠️ Cookies已超过7天，可能已过期")
                return None
        else:
            print("❌ 无效的cookies文件格式")
            return None

        # Validate cookies format
        if not validate_cookies_format(cookies):
            print("❌ Cookies格式验证失败")
            return None

        return cookies

    except FileNotFoundError:
        print(f"📂 未找到cookies文件: {filename}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Cookies文件格式错误: {e}")
        return None
    except Exception as e:
        print(f"❌ 加载cookies失败: {e}")
        return None


def validate_cookies_format(cookies: Any) -> bool:
    """
    Validate the format of cookies.

    Args:
        cookies (Any): The cookies to validate.

    Returns:
        bool: True if cookies format is valid, False otherwise.
    """
    if not isinstance(cookies, list):
        return False

    for cookie in cookies:
        if not isinstance(cookie, dict):
            return False
        if 'name' not in cookie or 'value' not in cookie:
            return False

    return True


def prepare_cookies_for_playwright(cookies: Any) -> List[Dict[str, Any]]:
    """
    Prepare cookies for use with Playwright by ensuring required fields are present.

    Args:
        cookies (Any): Raw cookies from file or browser.

    Returns:
        List[Dict[str, Any]]: Cookies formatted for Playwright.
    """
    prepared_cookies: List[Dict[str, Any]] = []

    if not isinstance(cookies, list):
        return prepared_cookies

    for cookie in cookies:
        if not isinstance(cookie, dict):
            continue

        # Ensure required fields exist
        if 'name' not in cookie or 'value' not in cookie:
            continue

        # Create a properly formatted cookie for Playwright
        playwright_cookie = {
            'name': cookie['name'],
            'value': cookie['value'],
            'domain': cookie.get('domain', ''),
            'path': cookie.get('path', '/'),
            'expires': cookie.get('expires', -1),
            'httpOnly': cookie.get('httpOnly', False),
            'secure': cookie.get('secure', False),
            'sameSite': cookie.get('sameSite', 'Lax')
        }

        # Only add cookies with valid domain
        if playwright_cookie['domain']:
            prepared_cookies.append(playwright_cookie)

    return prepared_cookies


def convert_cookies_to_playwright_format(cookies: Any) -> List["SetCookieParam"]:
    """
    Convert cookies to Playwright SetCookieParam format.

    Args:
        cookies (Any): Raw cookies from file or browser.

    Returns:
        List[SetCookieParam]: Cookies formatted for Playwright add_cookies method.
    """
    from playwright._impl._api_structures import SetCookieParam

    converted_cookies: List[SetCookieParam] = []

    if not isinstance(cookies, list):
        return converted_cookies

    for cookie in cookies:
        if not isinstance(cookie, dict):
            continue

        # Ensure required fields exist
        if 'name' not in cookie or 'value' not in cookie:
            continue

        # Create a properly formatted cookie for Playwright
        playwright_cookie: SetCookieParam = {
            'name': str(cookie['name']),
            'value': str(cookie['value']),
        }

        # Add optional fields if they exist
        if 'domain' in cookie and cookie['domain']:
            playwright_cookie['domain'] = str(cookie['domain'])
        if 'path' in cookie:
            playwright_cookie['path'] = str(cookie['path'])
        if 'expires' in cookie and isinstance(cookie['expires'], (int, float)):
            playwright_cookie['expires'] = float(cookie['expires'])
        if 'httpOnly' in cookie and isinstance(cookie['httpOnly'], bool):
            playwright_cookie['httpOnly'] = cookie['httpOnly']
        if 'secure' in cookie and isinstance(cookie['secure'], bool):
            playwright_cookie['secure'] = cookie['secure']
        if 'sameSite' in cookie and cookie['sameSite'] in ['Lax', 'None', 'Strict']:
            playwright_cookie['sameSite'] = cookie['sameSite']

        converted_cookies.append(playwright_cookie)

    return converted_cookies


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
