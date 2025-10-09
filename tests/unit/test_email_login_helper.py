"""
Comprehensive unit tests for EmailLoginHelper class.

Tests email login guidance, cookie management, browser session handling,
and interactive setup workflows.
"""
import pytest
from unittest.mock import Mock, patch, PropertyMock, ANY
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from src.tavily_register.email.login_helper import EmailLoginHelper
from src.tavily_register.config.settings import COOKIES_FILE
from tests.fixtures.sample_data import SAMPLE_COOKIES


@pytest.fixture
def helper(mocker) -> EmailLoginHelper:
    """Provides an EmailLoginHelper instance with a mocked page."""
    mock_page = mocker.Mock(spec=Page)
    mock_page.context = mocker.Mock()
    mock_page.url = "https://initial.url"
    return EmailLoginHelper(page=mock_page)


class TestEmailLoginHelperInit:
    """Test EmailLoginHelper initialization and setup."""

    def test_initialization(self, mocker):
        """Test EmailLoginHelper instance initialization."""
        mock_page = mocker.Mock(spec=Page)
        helper = EmailLoginHelper(page=mock_page)
        assert helper.page == mock_page


class TestEmailSiteExploration:
    """Test email site exploration functionality."""

    def test_explore_email_site_success(self, helper: EmailLoginHelper, mocker):
        """Test successful email site exploration."""
        mocker.patch.object(helper.page, 'goto')
        mocker.patch.object(helper.page, 'title', return_value="2925.com - Email Service")
        type(helper.page).url = mocker.PropertyMock(return_value="https://2925.com")
        mocker.patch.object(helper.page, 'query_selector_all', return_value=[])

        result = helper.explore_email_site()

        assert result is True
        helper.page.goto.assert_called()

    def test_explore_email_site_navigation_failure(self, helper: EmailLoginHelper, mocker):
        """Test email site exploration with navigation failure."""
        mocker.patch.object(helper.page, 'goto', side_effect=Exception("Navigation failed"))

        result = helper.explore_email_site()

        assert result is False

    def test_explore_email_site_timeout(self, helper: EmailLoginHelper, mocker):
        """Test email site exploration with timeout."""
        mocker.patch.object(helper.page, 'goto', side_effect=PlaywrightTimeoutError("Page load timeout"))

        result = helper.explore_email_site()

        assert result is False

    @patch('time.sleep')
    def test_explore_email_site_with_wait(self, mock_sleep, helper: EmailLoginHelper, mocker):
        """Test email site exploration includes waiting."""
        mocker.patch.object(helper.page, 'goto')
        mocker.patch.object(helper.page, 'title', return_value="Email Site")
        type(helper.page).url = mocker.PropertyMock(return_value="https://2925.com")
        mocker.patch.object(helper.page, 'query_selector_all', return_value=[])

        result = helper.explore_email_site()

        assert result is True
        mock_sleep.assert_called()


class TestManualLoginGuidance:
    """Test manual login guidance functionality."""

    @patch('builtins.input', return_value="y")
    @patch('src.tavily_register.email.login_helper.save_cookies', return_value=True)
    def test_manual_login_guide_success(self, mock_save_cookies, mock_input, helper: EmailLoginHelper):
        """Test successful manual login guidance."""
        mock_cookies = SAMPLE_COOKIES
        helper.page.context.cookies.return_value = mock_cookies

        result = helper.manual_login_guide()

        assert result is True
        mock_save_cookies.assert_called_with(mock_cookies, COOKIES_FILE)

    @patch('builtins.input', return_value="n")
    def test_manual_login_guide_user_cancels(self, mock_input, helper: EmailLoginHelper):
        """Test manual login guidance when user cancels."""
        result = helper.manual_login_guide()
        assert result is False

    @patch('builtins.input', return_value="y")
    @patch('src.tavily_register.email.login_helper.save_cookies', return_value=False)
    def test_manual_login_guide_cookie_save_failure(self, mock_save_cookies, mock_input, helper: EmailLoginHelper):
        """Test manual login guidance with cookie save failure."""
        helper.page.context.cookies.return_value = SAMPLE_COOKIES
        result = helper.manual_login_guide()
        assert result is False

    @patch('builtins.input', return_value="y")
    @patch('src.tavily_register.utils.helpers.save_cookies', return_value=False)
    def test_manual_login_guide_no_cookies(self, mock_save_cookies, mock_input, helper: EmailLoginHelper):
        """Test manual login guidance when no cookies are available."""
        helper.page.context.cookies.return_value = []
        result = helper.manual_login_guide()
        assert result is False


class TestInteractiveSetup:
    """Test interactive email setup workflow."""

    def test_interactive_email_setup_success(self, helper: EmailLoginHelper, mocker):
        """Test successful interactive email setup."""
        mocker.patch.object(helper, 'explore_email_site', return_value=True)
        mocker.patch.object(helper, 'manual_login_guide', return_value=True)

        result = helper.interactive_email_setup()

        assert result is True
        helper.explore_email_site.assert_called_once()
        helper.manual_login_guide.assert_called_once()

    def test_interactive_email_setup_exploration_failure(self, helper: EmailLoginHelper, mocker):
        """Test interactive setup with exploration failure."""
        mocker.patch.object(helper, 'explore_email_site', return_value=False)
        mocker.patch.object(helper, 'manual_login_guide')

        result = helper.interactive_email_setup()

        assert result is False
        helper.explore_email_site.assert_called_once()
        helper.manual_login_guide.assert_not_called()

    def test_interactive_email_setup_login_failure(self, helper: EmailLoginHelper, mocker):
        """Test interactive setup with login guidance failure."""
        mocker.patch.object(helper, 'explore_email_site', return_value=True)
        mocker.patch.object(helper, 'manual_login_guide', return_value=False)

        result = helper.interactive_email_setup()

        assert result is False
        helper.explore_email_site.assert_called_once()
        helper.manual_login_guide.assert_called_once()


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_handle_page_crash_during_exploration(self, helper: EmailLoginHelper, mocker):
        """Test handling page crash during site exploration."""
        mocker.patch.object(helper.page, 'goto', side_effect=Exception("Page crashed"))
        result = helper.explore_email_site()
        assert result is False

    def test_handle_network_timeout_during_setup(self, helper: EmailLoginHelper, mocker):
        """Test handling network timeout during setup."""
        mocker.patch.object(helper, 'explore_email_site', side_effect=PlaywrightTimeoutError("Network timeout"))
        with pytest.raises(PlaywrightTimeoutError):
            helper.interactive_email_setup()