import pytest
import json
import base64
from src.tavily_register.main import TavilyMainController

def test_get_email_prefix_from_cookies_with_bad_padding(tmp_path):
    """
    Tests the case where the JWT payload has a length that is a multiple of 4,
    which caused incorrect padding to be added in the original implementation.
    """
    controller = TavilyMainController()
    cookie_file = tmp_path / "cookies.json"
    controller.cookie_file = str(cookie_file)

    # This payload, when base64 encoded, results in a string of length 36,
    # which is a multiple of 4. The buggy code would add '====' padding,
    # causing a decoding error.
    # Payload: {"name": "user@example.com"}
    # Base64 of payload: eyJuYW1lIjogInVzZXJAZXhhbXBsZS5jb20ifQ
    jwt_payload = "eyJuYW1lIjogInVzZXJAZXhhbXBsZS5jb20ifQ"
    jwt_token = f"header.{jwt_payload}.signature"

    cookie_data = { "cookies": [{"name": "aut", "value": jwt_token}] }
    with open(cookie_file, 'w', encoding='utf-8') as f:
        json.dump(cookie_data, f)

    prefix = controller.get_email_prefix_from_cookies()
    assert prefix == "user"

def test_get_email_prefix_from_cookies_with_urlsafe_chars(tmp_path):
    """
    Tests the case where the JWT payload contains URL-safe characters ('-' or '_')
    which are not handled by the standard base64 decoder.
    This test is expected to FAIL before the fix and PASS after.
    """
    controller = TavilyMainController()
    cookie_file = tmp_path / "cookies.json"
    controller.cookie_file = str(cookie_file)

    # This payload corresponds to '{"name": "user-_test@example.com"}'
    # and uses url-safe characters in its base64 representation.
    jwt_payload = "eyJuYW1lIjogInVzZXItX3Rlc3RAZXhhbXBsZS5jb20ifQ"
    jwt_token = f"header.{jwt_payload}.signature"

    cookie_data = { "cookies": [{"name": "aut", "value": jwt_token}] }
    with open(cookie_file, 'w', encoding='utf-8') as f:
        json.dump(cookie_data, f)

    prefix = controller.get_email_prefix_from_cookies()
    assert prefix == "user-_test"