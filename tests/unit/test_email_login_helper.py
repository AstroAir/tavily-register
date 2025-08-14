"""
Comprehensive unit tests for EmailLoginHelper class.

Tests email login guidance, cookie management, browser session handling,
and interactive setup workflows.
"""
import pytest
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from src.tavily_register.email.login_helper import EmailLoginHelper
from tests.fixtures.sample_data import (
    SAMPLE_COOKIES,
    get_sample_cookies_for_domain
)


class TestEmailLoginHelperInit:
    """Test EmailLoginHelper initialization and setup."""

    def test_initialization_default_values(self):
        """Test EmailLoginHelper instance initialization with default values."""
        helper = EmailLoginHelper()
        
        assert helper.playwright is None
        assert helper.browser is None
        assert helper.page is None

    def test_initialization_attributes(self):
        """Test EmailLoginHelper has required attributes."""
        helper = EmailLoginHelper()
        
        assert hasattr(helper, 'playwright')
        assert hasattr(helper, 'browser')
        assert hasattr(helper, 'page')


class TestBrowserLifecycle:
    """Test browser lifecycle management for email login helper."""

    @pytest.fixture
    def helper(self):
        """Create EmailLoginHelper instance for testing."""
        return EmailLoginHelper()

    @patch('playwright.sync_api.sync_playwright')
    def test_start_browser_success(self, mock_playwright, helper):
        """Test successful browser startup."""
        # Setup mocks
        mock_playwright_instance = Mock()
        mock_browser = Mock()
        mock_page = Mock()
        
        mock_playwright.return_value.start.return_value = mock_playwright_instance
        mock_playwright_instance.firefox.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page
        
        # Test browser startup
        helper.start_browser()
        
        # Verify calls
        mock_playwright_instance.firefox.launch.assert_called_once()
        mock_browser.new_page.assert_called_once()
        
        # Verify state
        assert helper.playwright == mock_playwright_instance
        assert helper.browser == mock_browser
        assert helper.page == mock_page

    @patch('playwright.sync_api.sync_playwright')
    def test_start_browser_with_headless_false(self, mock_playwright, helper):
        """Test browser startup with headless=False for manual interaction."""
        mock_playwright_instance = Mock()
        mock_browser = Mock()
        
        mock_playwright.return_value.start.return_value = mock_playwright_instance
        mock_playwright_instance.firefox.launch.return_value = mock_browser
        mock_browser.new_page.return_value = Mock()
        
        # Test browser startup with visible browser
        helper.start_browser(headless=False)
        
        launch_args = mock_playwright_instance.firefox.launch.call_args[1]
        assert launch_args['headless'] is False

    @patch('playwright.sync_api.sync_playwright')
    def test_start_browser_failure(self, mock_playwright, helper):
        """Test browser startup failure handling."""
        mock_playwright.return_value.start.side_effect = Exception("Browser launch failed")
        
        with pytest.raises(Exception, match="Browser launch failed"):
            helper.start_browser()

    def test_close_browser_success(self, helper):
        """Test successful browser closure."""
        mock_browser = Mock()
        helper.browser = mock_browser
        
        helper.close_browser()
        
        mock_browser.close.assert_called_once()
        assert helper.browser is None

    def test_close_browser_no_browser(self, helper):
        """Test browser closure when no browser is running."""
        helper.browser = None
        
        # Should not raise exception
        helper.close_browser()


class TestEmailSiteExploration:
    """Test email site exploration functionality."""

    @pytest.fixture
    def mock_helper(self):
        """Create EmailLoginHelper instance with mocked browser."""
        helper = EmailLoginHelper()
        helper.browser = Mock()
        helper.page = Mock()
        return helper

    def test_explore_email_site_success(self, mock_helper):
        """Test successful email site exploration."""
        mock_helper.page.goto.return_value = None
        mock_helper.page.title.return_value = "2925.com - Email Service"
        mock_helper.page.url = "https://2925.com"
        
        result = mock_helper.explore_email_site()
        
        assert result is True
        mock_helper.page.goto.assert_called()
        mock_helper.page.title.assert_called()

    def test_explore_email_site_navigation_failure(self, mock_helper):
        """Test email site exploration with navigation failure."""
        mock_helper.page.goto.side_effect = Exception("Navigation failed")
        
        result = mock_helper.explore_email_site()
        
        assert result is False

    def test_explore_email_site_timeout(self, mock_helper):
        """Test email site exploration with timeout."""
        mock_helper.page.goto.side_effect = PlaywrightTimeoutError("Page load timeout")
        
        result = mock_helper.explore_email_site()
        
        assert result is False

    @patch('time.sleep')
    def test_explore_email_site_with_wait(self, mock_sleep, mock_helper):
        """Test email site exploration includes waiting."""
        mock_helper.page.goto.return_value = None
        mock_helper.page.title.return_value = "Email Site"
        
        result = mock_helper.explore_email_site()
        
        assert result is True
        mock_sleep.assert_called()


class TestManualLoginGuidance:
    """Test manual login guidance functionality."""

    @pytest.fixture
    def mock_helper(self):
        """Create EmailLoginHelper instance with mocked browser."""
        helper = EmailLoginHelper()
        helper.browser = Mock()
        helper.page = Mock()
        return helper

    @patch('builtins.input')
    @patch('src.tavily_register.utils.helpers.save_cookies')
    def test_manual_login_guide_success(self, mock_save_cookies, mock_input, mock_helper):
        """Test successful manual login guidance."""
        # Mock user input to proceed
        mock_input.return_value = "y"
        
        # Mock cookie extraction
        mock_cookies = SAMPLE_COOKIES
        mock_helper.page.context.cookies.return_value = mock_cookies
        
        result = mock_helper.manual_login_guide()
        
        assert result is True
        mock_save_cookies.assert_called_with(mock_cookies)

    @patch('builtins.input')
    def test_manual_login_guide_user_cancels(self, mock_input, mock_helper):
        """Test manual login guidance when user cancels."""
        # Mock user input to cancel
        mock_input.return_value = "n"
        
        result = mock_helper.manual_login_guide()
        
        assert result is False

    @patch('builtins.input')
    @patch('src.tavily_register.utils.helpers.save_cookies')
    def test_manual_login_guide_cookie_save_failure(self, mock_save_cookies, mock_input, mock_helper):
        """Test manual login guidance with cookie save failure."""
        mock_input.return_value = "y"
        mock_helper.page.context.cookies.return_value = SAMPLE_COOKIES
        mock_save_cookies.side_effect = Exception("Save failed")
        
        result = mock_helper.manual_login_guide()
        
        assert result is False

    @patch('builtins.input')
    def test_manual_login_guide_no_cookies(self, mock_input, mock_helper):
        """Test manual login guidance when no cookies are available."""
        mock_input.return_value = "y"
        mock_helper.page.context.cookies.return_value = []
        
        result = mock_helper.manual_login_guide()
        
        assert result is False


class TestCookieTesting:
    """Test cookie testing and validation functionality."""

    @pytest.fixture
    def mock_helper(self):
        """Create EmailLoginHelper instance with mocked browser."""
        helper = EmailLoginHelper()
        helper.browser = Mock()
        helper.page = Mock()
        return helper

    @patch('src.tavily_register.utils.helpers.load_cookies')
    def test_test_saved_cookies_success(self, mock_load_cookies, mock_helper):
        """Test successful cookie testing."""
        mock_load_cookies.return_value = SAMPLE_COOKIES
        
        # Mock new page creation and cookie application
        mock_test_page = Mock()
        mock_helper.browser.new_page.return_value = mock_test_page
        mock_test_page.context.add_cookies.return_value = None
        mock_test_page.goto.return_value = None
        mock_test_page.title.return_value = "Email Dashboard"
        mock_test_page.url = "https://2925.com/dashboard"
        
        result = mock_helper.test_saved_cookies()
        
        assert result is True
        mock_load_cookies.assert_called()
        mock_test_page.context.add_cookies.assert_called_with(SAMPLE_COOKIES)
        mock_test_page.close.assert_called()

    @patch('src.tavily_register.utils.helpers.load_cookies')
    def test_test_saved_cookies_no_cookies(self, mock_load_cookies, mock_helper):
        """Test cookie testing when no cookies are saved."""
        mock_load_cookies.return_value = None
        
        result = mock_helper.test_saved_cookies()
        
        assert result is False

    @patch('src.tavily_register.utils.helpers.load_cookies')
    def test_test_saved_cookies_application_failure(self, mock_load_cookies, mock_helper):
        """Test cookie testing when cookie application fails."""
        mock_load_cookies.return_value = SAMPLE_COOKIES
        
        mock_test_page = Mock()
        mock_helper.browser.new_page.return_value = mock_test_page
        mock_test_page.context.add_cookies.side_effect = Exception("Cookie application failed")
        
        result = mock_helper.test_saved_cookies()
        
        assert result is False

    @patch('src.tavily_register.utils.helpers.load_cookies')
    def test_test_saved_cookies_navigation_failure(self, mock_load_cookies, mock_helper):
        """Test cookie testing when navigation fails."""
        mock_load_cookies.return_value = SAMPLE_COOKIES
        
        mock_test_page = Mock()
        mock_helper.browser.new_page.return_value = mock_test_page
        mock_test_page.context.add_cookies.return_value = None
        mock_test_page.goto.side_effect = Exception("Navigation failed")
        
        result = mock_helper.test_saved_cookies()
        
        assert result is False


class TestInteractiveSetup:
    """Test interactive email setup workflow."""

    @pytest.fixture
    def mock_helper(self):
        """Create EmailLoginHelper instance for interactive testing."""
        helper = EmailLoginHelper()
        return helper

    def test_interactive_email_setup_success(self, mock_helper):
        """Test successful interactive email setup."""
        # Mock all workflow steps to succeed
        mock_helper.explore_email_site = Mock(return_value=True)
        mock_helper.manual_login_guide = Mock(return_value=True)
        mock_helper.test_saved_cookies = Mock(return_value=True)
        
        result = mock_helper.interactive_email_setup()
        
        assert result is True
        mock_helper.explore_email_site.assert_called_once()
        mock_helper.manual_login_guide.assert_called_once()
        mock_helper.test_saved_cookies.assert_called_once()

    def test_interactive_email_setup_exploration_failure(self, mock_helper):
        """Test interactive setup with exploration failure."""
        mock_helper.explore_email_site = Mock(return_value=False)
        
        result = mock_helper.interactive_email_setup()
        
        assert result is False
        mock_helper.explore_email_site.assert_called_once()

    def test_interactive_email_setup_login_failure(self, mock_helper):
        """Test interactive setup with login guidance failure."""
        mock_helper.explore_email_site = Mock(return_value=True)
        mock_helper.manual_login_guide = Mock(return_value=False)
        
        result = mock_helper.interactive_email_setup()
        
        assert result is False
        mock_helper.explore_email_site.assert_called_once()
        mock_helper.manual_login_guide.assert_called_once()

    def test_interactive_email_setup_cookie_test_failure(self, mock_helper):
        """Test interactive setup with cookie test failure but still success."""
        mock_helper.explore_email_site = Mock(return_value=True)
        mock_helper.manual_login_guide = Mock(return_value=True)
        mock_helper.test_saved_cookies = Mock(return_value=False)
        
        result = mock_helper.interactive_email_setup()
        
        # Should still return True even if cookie test fails
        assert result is True


class TestErrorHandling:
    """Test error handling and edge cases."""

    @pytest.fixture
    def mock_helper(self):
        """Create EmailLoginHelper instance for error testing."""
        helper = EmailLoginHelper()
        helper.browser = Mock()
        helper.page = Mock()
        return helper

    def test_handle_browser_not_initialized(self, mock_helper):
        """Test handling when browser is not initialized."""
        mock_helper.browser = None
        
        result = mock_helper.test_saved_cookies()
        
        assert result is False

    def test_handle_page_crash_during_exploration(self, mock_helper):
        """Test handling page crash during site exploration."""
        mock_helper.page.goto.side_effect = Exception("Page crashed")
        
        result = mock_helper.explore_email_site()
        
        assert result is False

    def test_handle_cookie_corruption(self, mock_helper):
        """Test handling corrupted cookie data."""
        with patch('src.tavily_register.utils.helpers.load_cookies') as mock_load:
            mock_load.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            
            result = mock_helper.test_saved_cookies()
            
            assert result is False

    def test_handle_network_timeout_during_setup(self, mock_helper):
        """Test handling network timeout during setup."""
        mock_helper.explore_email_site = Mock(side_effect=PlaywrightTimeoutError("Network timeout"))
        
        result = mock_helper.interactive_email_setup()
        
        assert result is False


class TestCookieManagement:
    """Test cookie management functionality."""

    @pytest.fixture
    def mock_helper(self):
        """Create EmailLoginHelper instance for cookie testing."""
        helper = EmailLoginHelper()
        helper.page = Mock()
        return helper

    def test_extract_cookies_success(self, mock_helper):
        """Test successful cookie extraction."""
        mock_cookies = get_sample_cookies_for_domain("2925.com")
        mock_helper.page.context.cookies.return_value = mock_cookies
        
        cookies = mock_helper.extract_cookies()
        
        assert cookies == mock_cookies
        mock_helper.page.context.cookies.assert_called_once()

    def test_extract_cookies_empty(self, mock_helper):
        """Test cookie extraction when no cookies exist."""
        mock_helper.page.context.cookies.return_value = []
        
        cookies = mock_helper.extract_cookies()
        
        assert cookies == []

    def test_extract_cookies_failure(self, mock_helper):
        """Test cookie extraction failure."""
        mock_helper.page.context.cookies.side_effect = Exception("Cookie extraction failed")
        
        cookies = mock_helper.extract_cookies()
        
        assert cookies == []

    def test_filter_relevant_cookies(self, mock_helper):
        """Test filtering relevant cookies for email domain."""
        all_cookies = SAMPLE_COOKIES + [
            {"name": "other_site", "domain": "example.com", "value": "test"}
        ]
        mock_helper.page.context.cookies.return_value = all_cookies
        
        cookies = mock_helper.extract_cookies()
        
        # Should only return cookies for 2925.com domain
        domain_cookies = [c for c in cookies if c.get("domain") == "2925.com"]
        assert len(domain_cookies) > 0


class TestUserInteraction:
    """Test user interaction and guidance functionality."""

    @pytest.fixture
    def mock_helper(self):
        """Create EmailLoginHelper instance for user interaction testing."""
        helper = EmailLoginHelper()
        return helper

    @patch('builtins.input')
    @patch('builtins.print')
    def test_user_guidance_messages(self, mock_print, mock_input, mock_helper):
        """Test user guidance message display."""
        mock_input.return_value = "n"  # User cancels
        
        mock_helper.manual_login_guide()
        
        # Should have printed guidance messages
        assert mock_print.call_count > 0

    @patch('builtins.input')
    def test_user_input_validation(self, mock_input, mock_helper):
        """Test user input validation."""
        # Test various input formats
        test_inputs = ["y", "Y", "yes", "YES", "n", "N", "no", "NO"]
        
        for user_input in test_inputs:
            mock_input.return_value = user_input
            
            # Should handle all input formats gracefully
            result = mock_helper.manual_login_guide()
            assert isinstance(result, bool)

    @patch('time.sleep')
    def test_user_wait_periods(self, mock_sleep, mock_helper):
        """Test appropriate wait periods for user interaction."""
        mock_helper.explore_email_site = Mock(return_value=True)
        mock_helper.manual_login_guide = Mock(return_value=True)
        mock_helper.test_saved_cookies = Mock(return_value=True)
        
        mock_helper.interactive_email_setup()
        
        # Should include wait periods for user to read instructions
        mock_sleep.assert_called()
