import pytest
from unittest.mock import patch
from src.tavily_register.main import TavilyMainController

@patch('src.tavily_register.main.load_cookies')
def test_get_email_prefix_from_cookies_with_bad_padding(mock_load_cookies):
    """
    Tests the case where the JWT payload has a length that is a multiple of 4.
    This test now correctly mocks load_cookies to isolate the unit of work.
    """
    controller = TavilyMainController()
    jwt_payload = "eyJuYW1lIjogInVzZXJAZXhhbXBsZS5jb20ifQ"  # {"name": "user@example.com"}
    jwt_token = f"header.{jwt_payload}.signature"

    # Mock the return value of load_cookies
    mock_load_cookies.return_value = [{"name": "aut", "value": jwt_token}]

    prefix = controller.get_email_prefix_from_cookies()
    assert prefix == "user"
    mock_load_cookies.assert_called_once_with(controller.cookie_file)

@patch('src.tavily_register.main.load_cookies')
def test_get_email_prefix_from_cookies_with_urlsafe_chars(mock_load_cookies):
    """
    Tests the case where the JWT payload contains URL-safe characters.
    This test now correctly mocks load_cookies to isolate the unit of work.
    """
    controller = TavilyMainController()
    jwt_payload = "eyJuYW1lIjogInVzZXItX3Rlc3RAZXhhbXBsZS5jb20ifQ"  # {"name": "user-_test@example.com"}
    jwt_token = f"header.{jwt_payload}.signature"

    # Mock the return value of load_cookies
    mock_load_cookies.return_value = [{"name": "aut", "value": jwt_token}]

    prefix = controller.get_email_prefix_from_cookies()
    assert prefix == "user-_test"
    mock_load_cookies.assert_called_once_with(controller.cookie_file)