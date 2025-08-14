"""
Comprehensive unit tests for IntelligentTavilyAutomation class.

Tests the intelligent automation module including browser lifecycle,
form interactions, email verification, API key extraction, and error handling.
"""
import pytest
import time
from unittest.mock import Mock, patch, MagicMock, call
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation
from tests.fixtures.sample_data import (
    SAMPLE_HTML_CONTENT,
    TEST_SELECTORS,
    SAMPLE_API_RESPONSES,
    get_sample_email_by_type
)


class TestIntelligentTavilyAutomationInit:
    """Test initialization and basic setup."""

    def test_initialization_default_values(self):
        """Test automation instance initialization with default values."""
        automation = IntelligentTavilyAutomation()
        
        assert automation.playwright is None
        assert automation.browser is None
        assert automation.page is None
        assert automation.email is None
        assert automation.email_prefix is None
        assert automation.password is None
        assert automation.debug is True

    def test_initialization_with_custom_prefix(self):
        """Test automation instance initialization with custom email prefix."""
        automation = IntelligentTavilyAutomation()
        automation.email_prefix = "custom_test"
        
        assert automation.email_prefix == "custom_test"


class TestBrowserLifecycle:
    """Test browser lifecycle management."""

    @pytest.fixture
    def automation(self):
        """Create automation instance for testing."""
        return IntelligentTavilyAutomation()

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
    def test_start_browser_with_different_options(self, mock_playwright, automation):
        """Test browser startup with different options."""
        mock_playwright_instance = Mock()
        mock_browser = Mock()
        
        mock_playwright.return_value.start.return_value = mock_playwright_instance
        mock_playwright_instance.firefox.launch.return_value = mock_browser
        mock_browser.new_page.return_value = Mock()
        
        # Test with headless=False
        automation.start_browser(headless=False)
        
        launch_args = mock_playwright_instance.firefox.launch.call_args[1]
        assert launch_args['headless'] is False

    @patch('playwright.sync_api.sync_playwright')
    def test_start_browser_failure(self, mock_playwright, automation):
        """Test browser startup failure handling."""
        mock_playwright.return_value.start.side_effect = Exception("Browser launch failed")
        
        with pytest.raises(Exception, match="Browser launch failed"):
            automation.start_browser()

    def test_close_browser_success(self, automation):
        """Test successful browser closure."""
        # Setup mock browser
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

    def test_close_browser_failure(self, automation):
        """Test browser closure failure handling."""
        mock_browser = Mock()
        mock_browser.close.side_effect = Exception("Close failed")
        automation.browser = mock_browser
        
        # Should handle exception gracefully
        automation.close_browser()
        assert automation.browser is None


class TestFormInteractions:
    """Test form filling and interaction methods."""

    @pytest.fixture
    def mock_automation(self):
        """Create automation instance with mocked browser components."""
        automation = IntelligentTavilyAutomation()
        automation.page = Mock()
        automation.email = "test@2925.com"
        automation.password = "TestPassword123!"
        return automation

    def test_fill_email_success(self, mock_automation):
        """Test successful email field filling."""
        mock_automation.page.wait_for_selector.return_value = Mock()
        mock_automation.page.fill.return_value = None
        
        result = mock_automation.fill_email_field("#email")
        
        assert result is True
        mock_automation.page.wait_for_selector.assert_called_with("#email", timeout=10000)
        mock_automation.page.fill.assert_called_with("#email", "test@2925.com")

    def test_fill_email_timeout(self, mock_automation):
        """Test email field filling with timeout."""
        mock_automation.page.wait_for_selector.side_effect = PlaywrightTimeoutError("Timeout")
        
        result = mock_automation.fill_email_field("#email")
        
        assert result is False

    def test_fill_password_success(self, mock_automation):
        """Test successful password field filling."""
        mock_automation.page.wait_for_selector.return_value = Mock()
        mock_automation.page.fill.return_value = None
        
        result = mock_automation.fill_password_field("#password")
        
        assert result is True
        mock_automation.page.wait_for_selector.assert_called_with("#password", timeout=10000)
        mock_automation.page.fill.assert_called_with("#password", "TestPassword123!")

    def test_click_element_success(self, mock_automation):
        """Test successful element clicking."""
        mock_automation.page.wait_for_selector.return_value = Mock()
        mock_automation.page.click.return_value = None
        
        result = mock_automation.click_element("button[type='submit']")
        
        assert result is True
        mock_automation.page.wait_for_selector.assert_called_with("button[type='submit']", timeout=10000)
        mock_automation.page.click.assert_called_with("button[type='submit']")

    def test_click_element_not_found(self, mock_automation):
        """Test clicking element that doesn't exist."""
        mock_automation.page.wait_for_selector.side_effect = PlaywrightTimeoutError("Element not found")
        
        result = mock_automation.click_element("button[type='submit']")
        
        assert result is False


class TestEmailGeneration:
    """Test email generation and management."""

    def test_generate_email_with_prefix(self):
        """Test email generation with custom prefix."""
        automation = IntelligentTavilyAutomation()
        automation.email_prefix = "test_user"
        
        email = automation.generate_email()
        
        assert email.startswith("test_user-")
        assert "@2925.com" in email
        assert len(email.split("-")[1].split("@")[0]) == 8  # Random suffix length

    def test_generate_email_without_prefix(self):
        """Test email generation without custom prefix."""
        automation = IntelligentTavilyAutomation()
        automation.email_prefix = None
        
        email = automation.generate_email()
        
        assert "@2925.com" in email
        assert "-" in email

    def test_generate_password(self):
        """Test password generation."""
        automation = IntelligentTavilyAutomation()
        
        password = automation.generate_password()
        
        assert isinstance(password, str)
        assert len(password) > 0


class TestNavigationMethods:
    """Test page navigation methods."""

    @pytest.fixture
    def mock_automation(self):
        """Create automation instance with mocked page."""
        automation = IntelligentTavilyAutomation()
        automation.page = Mock()
        return automation

    def test_navigate_to_signup_success(self, mock_automation):
        """Test successful navigation to signup page."""
        mock_automation.page.goto.return_value = None
        
        result = mock_automation.navigate_to_signup()
        
        assert result is True
        mock_automation.page.goto.assert_called_once()

    def test_navigate_to_signup_failure(self, mock_automation):
        """Test navigation failure to signup page."""
        mock_automation.page.goto.side_effect = Exception("Navigation failed")
        
        result = mock_automation.navigate_to_signup()
        
        assert result is False

    @patch('time.sleep')
    def test_wait_for_page_load(self, mock_sleep, mock_automation):
        """Test page load waiting mechanism."""
        mock_automation.wait_for_page_load(3)
        
        mock_sleep.assert_called_with(3)


class TestErrorHandling:
    """Test error handling and edge cases."""

    @pytest.fixture
    def mock_automation(self):
        """Create automation instance for error testing."""
        automation = IntelligentTavilyAutomation()
        automation.page = Mock()
        return automation

    def test_handle_network_error(self, mock_automation):
        """Test handling of network errors."""
        mock_automation.page.goto.side_effect = Exception("Network error")
        
        result = mock_automation.navigate_to_signup()
        
        assert result is False

    def test_handle_element_not_found(self, mock_automation):
        """Test handling when elements are not found."""
        mock_automation.page.wait_for_selector.side_effect = PlaywrightTimeoutError("Element not found")
        
        result = mock_automation.fill_email_field("#nonexistent")
        
        assert result is False

    def test_handle_browser_crash(self, mock_automation):
        """Test handling of browser crashes."""
        mock_automation.page.click.side_effect = Exception("Browser disconnected")
        
        result = mock_automation.click_element("button")
        
        assert result is False


class TestLoggingAndDebugging:
    """Test logging and debugging functionality."""

    @pytest.fixture
    def mock_automation(self):
        """Create automation instance with debug enabled."""
        automation = IntelligentTavilyAutomation()
        automation.debug = True
        return automation

    @patch('builtins.print')
    def test_log_action_with_debug(self, mock_print, mock_automation):
        """Test logging when debug is enabled."""
        mock_automation.log("Test message")

        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert "Test message" in call_args

    def test_log_action_without_debug(self):
        """Test logging when debug is disabled."""
        automation = IntelligentTavilyAutomation()
        automation.debug = False

        with patch('builtins.print') as mock_print:
            automation.log("Test message")
            mock_print.assert_not_called()


class TestAPIKeyExtraction:
    """Test API key extraction functionality."""

    @pytest.fixture
    def mock_automation(self):
        """Create automation instance with mocked page."""
        automation = IntelligentTavilyAutomation()
        automation.page = Mock()
        return automation

    def test_extract_api_key_success(self, mock_automation):
        """Test successful API key extraction."""
        mock_automation.page.wait_for_selector.return_value = Mock()
        mock_automation.page.inner_text.return_value = "tvly-dev-abc123def456"

        api_key = mock_automation.extract_api_key()

        assert api_key == "tvly-dev-abc123def456"
        mock_automation.page.wait_for_selector.assert_called()
        mock_automation.page.inner_text.assert_called()

    def test_extract_api_key_element_not_found(self, mock_automation):
        """Test API key extraction when element is not found."""
        mock_automation.page.wait_for_selector.side_effect = PlaywrightTimeoutError("Element not found")

        api_key = mock_automation.extract_api_key()

        assert api_key is None

    def test_extract_api_key_empty_text(self, mock_automation):
        """Test API key extraction with empty text."""
        mock_automation.page.wait_for_selector.return_value = Mock()
        mock_automation.page.inner_text.return_value = ""

        api_key = mock_automation.extract_api_key()

        assert api_key is None

    def test_extract_api_key_invalid_format(self, mock_automation):
        """Test API key extraction with invalid format."""
        mock_automation.page.wait_for_selector.return_value = Mock()
        mock_automation.page.inner_text.return_value = "invalid-key-format"

        api_key = mock_automation.extract_api_key()

        # Should still return the text even if format is unexpected
        assert api_key == "invalid-key-format"


class TestEmailVerificationWorkflow:
    """Test email verification workflow."""

    @pytest.fixture
    def mock_automation(self):
        """Create automation instance with mocked dependencies."""
        automation = IntelligentTavilyAutomation()
        automation.email = "test@2925.com"
        return automation

    @patch('src.tavily_register.core.intelligent_automation.EmailChecker')
    def test_handle_email_verification_success(self, mock_email_checker_class, mock_automation):
        """Test successful email verification workflow."""
        # Setup mock email checker
        mock_checker = Mock()
        mock_email_checker_class.return_value = mock_checker
        mock_checker.wait_for_email.return_value = "https://app.tavily.com/verify?token=abc123"

        # Mock page navigation and API key extraction
        mock_automation.page = Mock()
        mock_automation.page.goto.return_value = None
        mock_automation.extract_api_key = Mock(return_value="tvly-dev-test123")

        api_key = mock_automation.handle_email_verification_and_login()

        assert api_key == "tvly-dev-test123"
        mock_checker.wait_for_email.assert_called_with("test@2925.com", timeout=300)
        mock_automation.page.goto.assert_called_with("https://app.tavily.com/verify?token=abc123")

    @patch('src.tavily_register.core.intelligent_automation.EmailChecker')
    def test_handle_email_verification_timeout(self, mock_email_checker_class, mock_automation):
        """Test email verification timeout."""
        mock_checker = Mock()
        mock_email_checker_class.return_value = mock_checker
        mock_checker.wait_for_email.return_value = None  # Timeout

        api_key = mock_automation.handle_email_verification_and_login()

        assert api_key is None

    @patch('src.tavily_register.core.intelligent_automation.EmailChecker')
    def test_handle_email_verification_checker_failure(self, mock_email_checker_class, mock_automation):
        """Test email verification when checker fails to start."""
        mock_email_checker_class.side_effect = Exception("Checker failed to start")

        api_key = mock_automation.handle_email_verification_and_login()

        assert api_key is None


class TestCompleteAutomationWorkflow:
    """Test complete automation workflow integration."""

    @pytest.fixture
    def mock_automation(self):
        """Create fully mocked automation instance."""
        automation = IntelligentTavilyAutomation()
        automation.email_prefix = "test"
        return automation

    @patch('src.tavily_register.utils.helpers.save_api_key')
    def test_run_complete_automation_success(self, mock_save_api_key, mock_automation):
        """Test successful complete automation workflow."""
        # Mock all workflow steps
        mock_automation.run_registration = Mock(return_value=True)
        mock_automation.handle_email_verification_and_login = Mock(return_value="tvly-dev-success123")
        mock_automation.email = "test@2925.com"
        mock_automation.password = "TestPassword123!"

        api_key = mock_automation.run_complete_automation()

        assert api_key == "tvly-dev-success123"
        mock_automation.run_registration.assert_called_once()
        mock_automation.handle_email_verification_and_login.assert_called_once()
        mock_save_api_key.assert_called_with("test@2925.com", "tvly-dev-success123", "TestPassword123!")

    def test_run_complete_automation_registration_failure(self, mock_automation):
        """Test complete automation workflow with registration failure."""
        mock_automation.run_registration = Mock(return_value=False)

        api_key = mock_automation.run_complete_automation()

        assert api_key is None
        mock_automation.run_registration.assert_called_once()

    def test_run_complete_automation_verification_failure(self, mock_automation):
        """Test complete automation workflow with verification failure."""
        mock_automation.run_registration = Mock(return_value=True)
        mock_automation.handle_email_verification_and_login = Mock(return_value=None)

        api_key = mock_automation.run_complete_automation()

        assert api_key is None


class TestBoundaryConditions:
    """Test boundary conditions and edge cases."""

    def test_empty_email_prefix(self):
        """Test automation with empty email prefix."""
        automation = IntelligentTavilyAutomation()
        automation.email_prefix = ""

        email = automation.generate_email()

        assert "@2925.com" in email
        # Should handle empty prefix gracefully

    def test_very_long_email_prefix(self):
        """Test automation with very long email prefix."""
        automation = IntelligentTavilyAutomation()
        automation.email_prefix = "a" * 100  # Very long prefix

        email = automation.generate_email()

        assert email.startswith("a" * 100)
        assert "@2925.com" in email

    def test_special_characters_in_prefix(self):
        """Test automation with special characters in email prefix."""
        automation = IntelligentTavilyAutomation()
        automation.email_prefix = "test-user_123"

        email = automation.generate_email()

        assert email.startswith("test-user_123")
        assert "@2925.com" in email
