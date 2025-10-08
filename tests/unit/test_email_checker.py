"""
Comprehensive unit tests for EmailChecker class.

Tests email verification, link extraction, browser management,
and email waiting mechanisms.
"""
import pytest
from unittest.mock import Mock, patch, PropertyMock
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from src.tavily_register.email.checker import EmailChecker
from tests.fixtures.sample_data import (
    SAMPLE_COOKIES,
    get_sample_email_by_type
)

@pytest.fixture
def checker(page: Page) -> EmailChecker:
    """Provides an EmailChecker instance with a real page fixture."""
    return EmailChecker(page=page)


class TestEmailCheckerInit:
    """Test EmailChecker initialization and setup."""

    def test_initialization_with_page(self, page: Page):
        """Test EmailChecker instance initialization with a page object."""
        checker = EmailChecker(page=page)
        assert checker.page == page
        assert checker._own_browser is False

    def test_initialization_without_page(self):
        """Test EmailChecker instance initialization without a page object."""
        checker = EmailChecker()
        assert checker.page is None
        assert checker._own_browser is True
        assert hasattr(checker, 'playwright')
        assert hasattr(checker, 'browser')


class TestBrowserLifecycle:
    """Test browser lifecycle management for email checking."""

    def test_start_browser_if_own_browser(self):
        """Test that start_browser only runs if the checker owns the browser."""
        with patch('src.tavily_register.email.checker.sync_playwright') as mock_playwright:
            mock_playwright_instance = Mock()
            mock_browser = Mock()
            mock_page = Mock()
            mock_playwright.return_value.start.return_value = mock_playwright_instance
            mock_playwright_instance.firefox.launch.return_value = mock_browser
            mock_browser.new_page.return_value = mock_page

            checker = EmailChecker() # Owns browser
            checker.start_browser()

            mock_playwright_instance.firefox.launch.assert_called_once()
            assert checker.page is not None

    def test_start_browser_if_not_own_browser(self, page: Page):
        """Test that start_browser does nothing if a page is provided."""
        with patch('src.tavily_register.email.checker.sync_playwright') as mock_playwright:
            checker = EmailChecker(page=page)
            checker.start_browser()
            mock_playwright.return_value.start.assert_not_called()

    def test_close_browser_if_own_browser(self):
        """Test that close_browser only runs if the checker owns the browser."""
        with patch('src.tavily_register.email.checker.sync_playwright'):
            checker = EmailChecker()
            # mock the attributes that would be set by start_browser
            checker.playwright = Mock()
            checker.browser = Mock()
            checker.page = Mock()

            checker.close_browser()

            checker.page.close.assert_called_once()
            checker.browser.close.assert_called_once()
            checker.playwright.stop.assert_called_once()

    def test_close_browser_if_not_own_browser(self, page: Page):
        """Test that close_browser does nothing if a page is provided."""
        checker = EmailChecker(page=page)
        # mock page.close() to check it's not called
        page.close = Mock()
        checker.close_browser()
        page.close.assert_not_called()


class TestCookieManagement:
    """Test cookie loading and management."""

    @patch('src.tavily_register.email.checker.load_cookies')
    def test_load_email_page_with_cookies(self, mock_load_cookies, checker: EmailChecker, mocker):
        """Test loading email page with saved cookies."""
        mock_load_cookies.return_value = SAMPLE_COOKIES
        mocker.patch.object(checker.page.context, 'add_cookies')
        mocker.patch.object(checker.page, 'goto')
        mocker.patch.object(checker.page, 'reload')
        mocker.patch.object(checker.page, 'title', return_value="Email Page")
        mocker.patch.object(type(checker.page), 'url', new_callable=PropertyMock, return_value="https://www.2925.com/#/mailList")


        result = checker.load_email_page()

        assert result is True
        mock_load_cookies.assert_called_once()
        checker.page.context.add_cookies.assert_called_once()
        assert checker.page.goto.call_count == 2 # Once for domain, once for mailList

    @patch('src.tavily_register.email.checker.load_cookies')
    def test_load_email_page_no_cookies(self, mock_load_cookies, checker: EmailChecker, mocker):
        """Test loading email page when no cookies are available."""
        mock_load_cookies.return_value = None
        mocker.patch.object(checker.page.context, 'add_cookies')
        mocker.patch.object(checker.page, 'goto')
        mocker.patch.object(checker.page, 'title', return_value="Email Page")
        mocker.patch.object(type(checker.page), 'url', new_callable=PropertyMock, return_value="https://www.2925.com/#/mailList")


        result = checker.load_email_page()
        # This now returns True because it navigates to the page anyway
        assert result is True
        checker.page.context.add_cookies.assert_not_called()

    @patch('src.tavily_register.email.checker.load_cookies')
    def test_load_email_page_cookie_error(self, mock_load_cookies, checker: EmailChecker, mocker):
        """Test loading email page when cookie loading fails."""
        mock_load_cookies.return_value = SAMPLE_COOKIES
        mocker.patch.object(checker.page.context, 'add_cookies', side_effect=Exception("Cookie error"))
        mocker.patch.object(checker.page, 'goto')
        mocker.patch.object(checker.page, 'reload')
        mocker.patch.object(type(checker.page), 'url', new_callable=PropertyMock, return_value="https://www.2925.com/#/mailList")

        # The function now catches the exception and continues
        result = checker.load_email_page()

        assert result is True # It still proceeds to load the page
        checker.page.context.add_cookies.assert_called()


class TestEmailDetection:
    """Test email detection and parsing functionality."""

    def test_find_emails_on_page_success(self, checker: EmailChecker, mocker):
        """Test successful email detection on page."""
        mock_email_elements = [
            Mock(), Mock()
        ]
        for el in mock_email_elements:
            el.inner_text.return_value = "From: noreply@tavily.com\nSubject: Verify your email"
            el.query_selector_all.return_value = []
            el.get_attribute.return_value = ""

        mocker.patch.object(checker.page, 'query_selector_all', return_value=mock_email_elements)
        emails = checker.find_emails_on_page()

        assert len(emails) == 2
        assert "noreply@tavily.com" in emails[0]['text']

    def test_find_emails_on_page_no_emails(self, checker: EmailChecker, mocker):
        """Test email detection when no emails are found."""
        mocker.patch.object(checker.page, 'query_selector_all', return_value=[])
        emails = checker.find_emails_on_page()
        assert emails == []

    def test_find_emails_on_page_error(self, checker: EmailChecker, mocker):
        """Test email detection with page error."""
        mocker.patch.object(checker.page, 'query_selector_all', side_effect=Exception("Page error"))
        emails = checker.find_emails_on_page()
        assert emails == []


class TestVerificationLinkExtraction:
    """Test verification link extraction functionality."""

    def test_extract_verification_link_tavily(self, checker: EmailChecker):
        """Test extracting Tavily verification link."""
        email_content = "Please verify your email by clicking: https://auth.tavily.com/u/email-verification?ticket=abc123def456"
        link = checker.extract_link_from_text(email_content)
        assert link == "https://auth.tavily.com/u/email-verification?ticket=abc123def456"

    def test_extract_verification_link_multiple_links(self, checker: EmailChecker):
        """Test extracting verification link when multiple links are present."""
        email_content = """
        Visit our website: https://tavily.com
        Verify your email: https://app.tavily.com/verify?token=xyz789
        Unsubscribe: https://tavily.com/unsubscribe
        """
        link = checker.extract_link_from_text(email_content)
        assert link == "https://app.tavily.com/verify?token=xyz789"

    def test_extract_verification_link_no_verification_link(self, checker: EmailChecker):
        """Test extracting verification link when none exists."""
        email_content = "Welcome to Tavily! Visit us at https://tavily.com"
        link = checker.extract_link_from_text(email_content)
        assert link is None

    def test_extract_verification_link_malformed_url(self, checker: EmailChecker):
        """Test extracting verification link with malformed URL."""
        email_content = "Verify here: app.tavily.com/verify?token=invalid"
        link = checker.extract_link_from_text(email_content)
        assert link is None

    def test_extract_verification_link_different_patterns(self, checker: EmailChecker):
        """Test extracting verification links with different URL patterns."""
        test_cases = [
            "https://auth.tavily.com/u/email-verification?ticket=abc123",
            "https://app.tavily.com/verify?code=def456",
        ]
        expected = [
            "https://auth.tavily.com/u/email-verification?ticket=abc123",
            "https://app.tavily.com/verify?code=def456",
        ]
        for i, email_content in enumerate(test_cases):
            link = checker.extract_link_from_text(f"Click here: {email_content}")
            assert link == expected[i]


class TestEmailWaiting:
    """Test email waiting and polling mechanisms."""

    @patch('time.sleep')
    def test_check_for_tavily_email_success(self, mock_sleep, checker: EmailChecker):
        """Test successful email waiting."""
        checker.find_emails_on_page = Mock(side_effect=[
            [],
            [{'text': 'From: noreply@tavily.com\nSubject: Verify\nhttps://app.tavily.com/verify?token=abc123', 'is_unread': True, 'element': Mock(), 'index': 0}]
        ])
        checker.process_email_with_alias_check = Mock(return_value="https://app.tavily.com/verify?token=abc123")
        checker.refresh_email_list = Mock()

        link = checker.check_for_tavily_email("test@2925.com", max_retries=2, wait_interval=1)

        assert link == "https://app.tavily.com/verify?token=abc123"
        assert checker.find_emails_on_page.call_count == 2
        checker.refresh_email_list.assert_called_once()

    @patch('time.sleep')
    def test_check_for_tavily_email_timeout(self, mock_sleep, checker: EmailChecker):
        """Test email waiting timeout."""
        checker.find_emails_on_page = Mock(return_value=[])
        checker.refresh_email_list = Mock()
        link = checker.check_for_tavily_email("test@2925.com", max_retries=2, wait_interval=1)
        assert link is None
        assert checker.find_emails_on_page.call_count == 2

    @patch('time.sleep')
    def test_check_for_tavily_email_wrong_recipient(self, mock_sleep, checker: EmailChecker):
        """Test email waiting for wrong recipient."""
        email_info = {'text': 'To: other@example.com\nFrom: noreply@tavily.com\nSubject: Verify', 'is_unread':True, 'element': Mock(), 'index': 0}
        checker.find_emails_on_page = Mock(return_value=[email_info])
        checker.process_email_with_alias_check = Mock(return_value=None) # Alias check fails
        checker.refresh_email_list = Mock()

        link = checker.check_for_tavily_email("test@2925.com", max_retries=2, wait_interval=1)
        assert link is None

    def test_check_for_tavily_email_immediate_success(self, checker: EmailChecker):
        """Test email waiting with immediate success."""
        email_info = {'text': 'To: test@2925.com\nFrom: noreply@tavily.com\nSubject: Verify\nhttps://app.tavily.com/verify?token=abc123', 'is_unread': True, 'element': Mock(), 'index': 0}
        checker.find_emails_on_page = Mock(return_value=[email_info])
        checker.process_email_with_alias_check = Mock(return_value="https://app.tavily.com/verify?token=abc123")
        checker.refresh_email_list = Mock()

        link = checker.check_for_tavily_email("test@2925.com", max_retries=1)
        assert link == "https://app.tavily.com/verify?token=abc123"
        checker.find_emails_on_page.assert_called_once()


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_handle_page_load_error(self, checker: EmailChecker, mocker):
        """Test handling page load errors."""
        mocker.patch.object(checker.page, 'goto', side_effect=Exception("Page load failed"))
        result = checker.load_email_page()
        assert result is False

    def test_handle_email_parsing_error(self, checker: EmailChecker, mocker):
        """Test handling email parsing errors."""
        mocker.patch.object(checker.page, 'query_selector_all', side_effect=Exception("Parsing failed"))
        emails = checker.find_emails_on_page()
        assert emails == []

    def test_handle_browser_crash_during_wait(self, checker: EmailChecker, mocker):
        """Test handling browser crash during email waiting."""
        mocker.patch.object(checker, 'find_emails_on_page', side_effect=Exception("Browser crashed"))
        link = checker.check_for_tavily_email("test@2925.com", max_retries=1)
        assert link is None


class TestIntegrationScenarios:
    """Test integration scenarios and workflows."""

    @patch('src.tavily_register.email.checker.load_cookies')
    def test_complete_email_verification_workflow(self, mock_load_cookies, checker: EmailChecker, mocker):
        """Test complete email verification workflow."""
        mock_load_cookies.return_value = SAMPLE_COOKIES
        mocker.patch.object(checker.page.context, 'add_cookies')
        mocker.patch.object(checker.page, 'goto')
        mocker.patch.object(checker.page, 'reload')
        mocker.patch.object(checker.page, 'title', return_value="Email Page")
        mocker.patch.object(type(checker.page), 'url', new_callable=PropertyMock, return_value="https://www.2925.com/#/mailList")

        verification_email = get_sample_email_by_type("verification")
        email_info = {'text': f"To: test@2925.com\n{verification_email['body']}", 'is_unread': True, 'element': Mock(), 'index': 0}
        mocker.patch.object(checker, 'find_emails_on_page', return_value=[email_info])
        mocker.patch.object(checker, 'process_email_with_alias_check', return_value="https://app.tavily.com/verify?token=abc123")

        load_result = checker.load_email_page()
        verification_link = checker.check_for_tavily_email("test@2925.com", max_retries=1)

        assert load_result is True
        assert verification_link == "https://app.tavily.com/verify?token=abc123"

    @patch('time.sleep')
    def test_email_verification_with_retry(self, mock_sleep, checker: EmailChecker):
        """Test email verification with retry mechanism."""
        verification_email_info = {
            'text': 'To: test@2925.com\nFrom: noreply@tavily.com\nhttps://app.tavily.com/verify?token=retry123',
            'is_unread': True, 'element': Mock(), 'index': 0
        }
        checker.find_emails_on_page = Mock(side_effect=[[], [], [verification_email_info]])
        checker.process_email_with_alias_check = Mock(return_value="https://app.tavily.com/verify?token=retry123")
        checker.refresh_email_list = Mock()

        link = checker.check_for_tavily_email("test@2925.com", max_retries=3, wait_interval=1)

        assert link == "https://app.tavily.com/verify?token=retry123"
        assert checker.find_emails_on_page.call_count == 3


class TestDialogHandling:
    """Test dialog handling functionality."""

    def test_handle_dialog_accept(self, checker: EmailChecker):
        """Test that the dialog is accepted for specific messages."""
        mock_dialog_accept = Mock()
        mock_dialog_accept.message = "第三方网站跳转提醒"
        mock_dialog_accept.accept = Mock()
        mock_dialog_accept.dismiss = Mock()

        checker.handle_dialog(mock_dialog_accept)
        mock_dialog_accept.accept.assert_called_once()
        mock_dialog_accept.dismiss.assert_not_called()

        mock_dialog_leave = Mock()
        mock_dialog_leave.message = "即将离开"
        mock_dialog_leave.accept = Mock()
        mock_dialog_leave.dismiss = Mock()

        checker.handle_dialog(mock_dialog_leave)
        mock_dialog_leave.accept.assert_called_once()
        mock_dialog_leave.dismiss.assert_not_called()

    def test_handle_dialog_dismiss(self, checker: EmailChecker):
        """Test that the dialog is dismissed for other messages."""
        mock_dialog = Mock()
        mock_dialog.message = "Some other dialog"
        mock_dialog.accept = Mock()
        mock_dialog.dismiss = Mock()

        checker.handle_dialog(mock_dialog)
        mock_dialog.dismiss.assert_called_once()
        mock_dialog.accept.assert_not_called()

    def test_handle_dialog_exception(self, checker: EmailChecker):
        """Test exception handling during dialog processing."""
        mock_dialog = Mock()
        mock_dialog.message = "第三方网站跳转提醒"
        mock_dialog.accept.side_effect = Exception("Accept failed")
        mock_dialog.dismiss = Mock() # Add dismiss mock to avoid AttributeError

        # Should not raise an exception
        checker.handle_dialog(mock_dialog)
        mock_dialog.dismiss.assert_called_once()


class TestEmailListManagement:
    """Test email list management functions like refresh and back."""

    def test_refresh_email_list_reload(self, checker: EmailChecker, mocker):
        """Test that refresh_email_list calls page.reload()."""
        mocker.patch.object(checker.page, 'reload')
        mocker.patch.object(checker.page, 'query_selector', return_value=None) # No button found

        checker.refresh_email_list()

        checker.page.reload.assert_called_once()

    def test_refresh_email_list_with_button(self, checker: EmailChecker, mocker):
        """Test that refresh_email_list clicks a refresh button if found."""
        mock_button = Mock()
        mocker.patch.object(checker.page, 'reload')
        mocker.patch.object(checker.page, 'query_selector', return_value=mock_button)

        checker.refresh_email_list()

        checker.page.reload.assert_called_once()
        mock_button.click.assert_called_once()

    def test_refresh_email_list_exception(self, checker: EmailChecker, mocker):
        """Test exception handling in refresh_email_list."""
        mocker.patch.object(checker.page, 'reload', side_effect=Exception("Reload failed"))
        # Should not raise an exception
        checker.refresh_email_list()
        assert True # If it doesn't crash, it passes.

    def test_return_to_email_list_back_button(self, checker: EmailChecker, mocker):
        """Test return_to_email_list by clicking a back button."""
        mock_button = Mock()
        mocker.patch.object(checker.page, 'query_selector', return_value=mock_button)
        mocker.patch.object(checker.page, 'go_back')

        checker.return_to_email_list()

        mock_button.click.assert_called_once()
        checker.page.go_back.assert_not_called()

    def test_return_to_email_list_go_back(self, checker: EmailChecker, mocker):
        """Test return_to_email_list by using page.go_back()."""
        mocker.patch.object(checker.page, 'query_selector', return_value=None)
        mocker.patch.object(checker.page, 'go_back')

        checker.return_to_email_list()

        checker.page.go_back.assert_called_once()

    def test_return_to_email_list_exception(self, checker: EmailChecker, mocker):
        """Test exception handling in return_to_email_list."""
        mocker.patch.object(checker.page, 'query_selector', side_effect=Exception("Query failed"))
        mocker.patch.object(checker.page, 'go_back')

        checker.return_to_email_list()

        # It should fall back to go_back
        checker.page.go_back.assert_called_once()