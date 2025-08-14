"""
Comprehensive unit tests for TavilyAutomation class.

Tests the traditional automation module including browser lifecycle,
HTML collection, element detection, and fallback mechanisms.
"""
import pytest
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from src.tavily_register.core.traditional_automation import TavilyAutomation
from tests.fixtures.sample_data import (
    SAMPLE_HTML_CONTENT,
    TEST_SELECTORS,
    MOCK_BROWSER_RESPONSES
)


class TestTavilyAutomationInit:
    """Test initialization and basic setup."""

    def test_initialization_default_values(self):
        """Test automation instance initialization with default values."""
        automation = TavilyAutomation()
        
        assert automation.playwright is None
        assert automation.browser is None
        assert automation.page is None
        assert automation.email is None
        assert automation.email_prefix is None
        assert automation.password is None
        assert automation.html_log == []

    def test_initialization_with_custom_prefix(self):
        """Test automation instance initialization with custom email prefix."""
        automation = TavilyAutomation()
        automation.email_prefix = "traditional_test"
        
        assert automation.email_prefix == "traditional_test"


class TestBrowserLifecycle:
    """Test browser lifecycle management for traditional automation."""

    @pytest.fixture
    def automation(self):
        """Create automation instance for testing."""
        return TavilyAutomation()

    @patch('playwright.sync_api.sync_playwright')
    def test_start_browser_success(self, mock_playwright, automation):
        """Test successful browser startup."""
        # Setup mocks
        mock_playwright_instance = Mock()
        mock_browser = Mock()
        mock_page = Mock()
        
        mock_playwright.return_value.start.return_value = mock_playwright_instance
        mock_playwright_instance.firefox.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page
        
        # Test browser startup
        automation.start_browser(headless=True)
        
        # Verify calls
        mock_playwright_instance.firefox.launch.assert_called_once()
        launch_args = mock_playwright_instance.firefox.launch.call_args[1]
        assert launch_args['headless'] is True
        
        mock_browser.new_page.assert_called_once()
        
        # Verify state
        assert automation.playwright == mock_playwright_instance
        assert automation.browser == mock_browser
        assert automation.page == mock_page

    @patch('playwright.sync_api.sync_playwright')
    def test_start_browser_failure(self, mock_playwright, automation):
        """Test browser startup failure handling."""
        mock_playwright.return_value.start.side_effect = Exception("Browser launch failed")
        
        with pytest.raises(Exception, match="Browser launch failed"):
            automation.start_browser()

    def test_close_browser_success(self, automation):
        """Test successful browser closure."""
        mock_browser = Mock()
        automation.browser = mock_browser
        
        automation.close_browser()
        
        mock_browser.close.assert_called_once()
        assert automation.browser is None

    def test_close_browser_no_browser(self, automation):
        """Test browser closure when no browser is running."""
        automation.browser = None
        
        # Should not raise exception
        automation.close_browser()


class TestHTMLCollection:
    """Test HTML collection and logging functionality."""

    @pytest.fixture
    def mock_automation(self):
        """Create automation instance with mocked page."""
        automation = TavilyAutomation()
        automation.page = Mock()
        return automation

    def test_collect_element_info_success(self, mock_automation):
        """Test successful element information collection."""
        mock_element = Mock()
        mock_element.inner_html.return_value = "<input id='test' type='text'>"
        mock_element.get_attribute.return_value = "test-value"
        
        mock_automation.collect_element_info(mock_element, "fill", "test_input")
        
        assert len(mock_automation.html_log) == 1
        log_entry = mock_automation.html_log[0]
        assert log_entry["action"] == "fill"
        assert log_entry["element_name"] == "test_input"
        assert log_entry["html"] == "<input id='test' type='text'>"

    def test_collect_element_info_failure(self, mock_automation):
        """Test element information collection with failure."""
        mock_element = Mock()
        mock_element.inner_html.side_effect = Exception("Element access failed")
        
        # Should handle exception gracefully
        mock_automation.collect_element_info(mock_element, "click", "test_button")
        
        assert len(mock_automation.html_log) == 1
        log_entry = mock_automation.html_log[0]
        assert log_entry["action"] == "click"
        assert log_entry["element_name"] == "test_button"
        assert "error" in log_entry

    def test_save_html_log_success(self, mock_automation):
        """Test successful HTML log saving."""
        # Add some test data to log
        mock_automation.html_log = [
            {"action": "fill", "element_name": "email", "html": "<input>"},
            {"action": "click", "element_name": "submit", "html": "<button>"}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name
        
        try:
            mock_automation.save_html_log(tmp_path)
            
            # Verify file was created and contains correct data
            assert os.path.exists(tmp_path)
            with open(tmp_path, 'r') as f:
                saved_data = json.load(f)
            
            assert len(saved_data) == 2
            assert saved_data[0]["action"] == "fill"
            assert saved_data[1]["action"] == "click"
        finally:
            os.unlink(tmp_path)

    def test_save_html_log_empty(self, mock_automation):
        """Test HTML log saving with empty log."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name
        
        try:
            mock_automation.save_html_log(tmp_path)
            
            with open(tmp_path, 'r') as f:
                saved_data = json.load(f)
            
            assert saved_data == []
        finally:
            os.unlink(tmp_path)


class TestNavigationMethods:
    """Test navigation methods for traditional automation."""

    @pytest.fixture
    def mock_automation(self):
        """Create automation instance with mocked page."""
        automation = TavilyAutomation()
        automation.page = Mock()
        return automation

    def test_navigate_to_signup_success(self, mock_automation):
        """Test successful navigation to signup page."""
        mock_automation.page.goto.return_value = None
        mock_automation.page.wait_for_selector.return_value = Mock()
        
        result = mock_automation.navigate_to_signup()
        
        assert result is True
        mock_automation.page.goto.assert_called()

    def test_navigate_to_signup_failure(self, mock_automation):
        """Test navigation failure to signup page."""
        mock_automation.page.goto.side_effect = Exception("Navigation failed")
        
        result = mock_automation.navigate_to_signup()
        
        assert result is False

    def test_navigate_to_signup_with_fallback(self, mock_automation):
        """Test navigation with fallback to direct signup URL."""
        # First attempt fails to find signup button
        mock_automation.page.wait_for_selector.side_effect = [
            PlaywrightTimeoutError("Button not found"),
            Mock()  # Second attempt succeeds
        ]
        mock_automation.page.goto.return_value = None
        
        result = mock_automation.navigate_to_signup()
        
        assert result is True
        # Should call goto twice - once for main page, once for direct signup
        assert mock_automation.page.goto.call_count >= 1


class TestFormFilling:
    """Test form filling functionality."""

    @pytest.fixture
    def mock_automation(self):
        """Create automation instance with mocked page and credentials."""
        automation = TavilyAutomation()
        automation.page = Mock()
        automation.email = "test@2925.com"
        automation.password = "TestPassword123!"
        return automation

    def test_fill_registration_form_success(self, mock_automation):
        """Test successful registration form filling."""
        # Mock successful element finding and filling
        mock_email_input = Mock()
        mock_password_input = Mock()
        mock_submit_button = Mock()
        
        mock_automation.page.wait_for_selector.side_effect = [
            mock_email_input,
            mock_password_input,
            mock_submit_button
        ]
        
        result = mock_automation.fill_registration_form()
        
        assert result is True
        mock_email_input.fill.assert_called_with("test@2925.com")
        mock_password_input.fill.assert_called_with("TestPassword123!")
        mock_submit_button.click.assert_called_once()

    def test_fill_registration_form_email_not_found(self, mock_automation):
        """Test form filling when email input is not found."""
        mock_automation.page.wait_for_selector.side_effect = PlaywrightTimeoutError("Email input not found")
        
        result = mock_automation.fill_registration_form()
        
        assert result is False

    def test_fill_registration_form_password_not_found(self, mock_automation):
        """Test form filling when password input is not found."""
        mock_email_input = Mock()
        mock_automation.page.wait_for_selector.side_effect = [
            mock_email_input,
            PlaywrightTimeoutError("Password input not found")
        ]
        
        result = mock_automation.fill_registration_form()
        
        assert result is False

    def test_fill_registration_form_submit_not_found(self, mock_automation):
        """Test form filling when submit button is not found."""
        mock_email_input = Mock()
        mock_password_input = Mock()
        
        mock_automation.page.wait_for_selector.side_effect = [
            mock_email_input,
            mock_password_input,
            PlaywrightTimeoutError("Submit button not found")
        ]
        
        # Should try alternative submission method (Enter key)
        result = mock_automation.fill_registration_form()
        
        # Should still succeed with fallback
        assert result is True
        mock_password_input.press.assert_called_with('Enter')


class TestElementDetection:
    """Test element detection strategies."""

    @pytest.fixture
    def mock_automation(self):
        """Create automation instance with mocked page."""
        automation = TavilyAutomation()
        automation.page = Mock()
        return automation

    def test_find_element_with_multiple_selectors(self, mock_automation):
        """Test finding element with multiple selector strategies."""
        mock_element = Mock()
        
        # First selector fails, second succeeds
        mock_automation.page.wait_for_selector.side_effect = [
            PlaywrightTimeoutError("First selector failed"),
            mock_element
        ]
        
        selectors = ["#email", "input[type='email']"]
        element = mock_automation.find_element_with_selectors(selectors)
        
        assert element == mock_element
        assert mock_automation.page.wait_for_selector.call_count == 2

    def test_find_element_all_selectors_fail(self, mock_automation):
        """Test finding element when all selectors fail."""
        mock_automation.page.wait_for_selector.side_effect = PlaywrightTimeoutError("Not found")
        
        selectors = ["#email", "input[type='email']", ".email-input"]
        element = mock_automation.find_element_with_selectors(selectors)
        
        assert element is None
        assert mock_automation.page.wait_for_selector.call_count == 3


class TestErrorHandling:
    """Test error handling and recovery mechanisms."""

    @pytest.fixture
    def mock_automation(self):
        """Create automation instance for error testing."""
        automation = TavilyAutomation()
        automation.page = Mock()
        return automation

    def test_handle_network_timeout(self, mock_automation):
        """Test handling of network timeouts."""
        mock_automation.page.goto.side_effect = PlaywrightTimeoutError("Network timeout")
        
        result = mock_automation.navigate_to_signup()
        
        assert result is False

    def test_handle_element_interaction_failure(self, mock_automation):
        """Test handling of element interaction failures."""
        mock_element = Mock()
        mock_element.fill.side_effect = Exception("Element interaction failed")
        mock_automation.page.wait_for_selector.return_value = mock_element
        
        result = mock_automation.fill_email_field("#email")
        
        assert result is False

    def test_handle_browser_disconnection(self, mock_automation):
        """Test handling of browser disconnection."""
        mock_automation.page.goto.side_effect = Exception("Browser disconnected")
        
        result = mock_automation.navigate_to_signup()
        
        assert result is False


class TestWaitingMechanisms:
    """Test waiting and timing mechanisms."""

    @pytest.fixture
    def mock_automation(self):
        """Create automation instance for timing tests."""
        automation = TavilyAutomation()
        automation.page = Mock()
        return automation

    @patch('time.sleep')
    def test_wait_for_page_load(self, mock_sleep, mock_automation):
        """Test page load waiting mechanism."""
        mock_automation.wait_for_page_load(5)
        
        mock_sleep.assert_called_with(5)

    def test_wait_for_element_with_timeout(self, mock_automation):
        """Test waiting for element with custom timeout."""
        mock_element = Mock()
        mock_automation.page.wait_for_selector.return_value = mock_element
        
        element = mock_automation.wait_for_element("#test", timeout=5000)
        
        assert element == mock_element
        mock_automation.page.wait_for_selector.assert_called_with("#test", timeout=5000)

    def test_wait_for_element_timeout(self, mock_automation):
        """Test waiting for element that times out."""
        mock_automation.page.wait_for_selector.side_effect = PlaywrightTimeoutError("Timeout")
        
        element = mock_automation.wait_for_element("#test", timeout=1000)
        
        assert element is None
