"""
Comprehensive unit tests for EmailChecker class.

Tests email verification, link extraction, browser management,
and email waiting mechanisms.
"""
import pytest
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from src.tavily_register.email.checker import EmailChecker
from tests.fixtures.sample_data import (
    SAMPLE_EMAILS,
    SAMPLE_COOKIES,
    SAMPLE_HTML_CONTENT,
    get_sample_email_by_type
)


class TestEmailCheckerInit:
    """Test EmailChecker initialization and setup."""

    def test_initialization_default_values(self):
        """Test EmailChecker instance initialization with default values."""
        checker = EmailChecker()
        
        assert checker.playwright is None
        assert checker.browser is None
        assert checker.page is None

    def test_initialization_with_custom_config(self):
        """Test EmailChecker initialization with custom configuration."""
        checker = EmailChecker()
        
        # Should initialize with default configuration
        assert hasattr(checker, 'playwright')
        assert hasattr(checker, 'browser')
        assert hasattr(checker, 'page')


class TestBrowserLifecycle:
    """Test browser lifecycle management for email checking."""

    @pytest.fixture
    def checker(self):
        """Create EmailChecker instance for testing."""
        return EmailChecker()

    @patch('playwright.sync_api.sync_playwright')
    def test_start_browser_success(self, mock_playwright, checker):
        """Test successful browser startup."""
        # Setup mocks
        mock_playwright_instance = Mock()
        mock_browser = Mock()
        mock_page = Mock()
        
        mock_playwright.return_value.start.return_value = mock_playwright_instance
        mock_playwright_instance.firefox.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page
        
        # Test browser startup
        checker.start_browser()
        
        # Verify calls
        mock_playwright_instance.firefox.launch.assert_called_once()
        mock_browser.new_page.assert_called_once()
        
        # Verify state
        assert checker.playwright == mock_playwright_instance
        assert checker.browser == mock_browser
        assert checker.page == mock_page

    @patch('playwright.sync_api.sync_playwright')
    def test_start_browser_failure(self, mock_playwright, checker):
        """Test browser startup failure handling."""
        mock_playwright.return_value.start.side_effect = Exception("Browser launch failed")
        
        with pytest.raises(Exception, match="Browser launch failed"):
            checker.start_browser()

    def test_close_browser_success(self, checker):
        """Test successful browser closure."""
        mock_browser = Mock()
        checker.browser = mock_browser
        
        checker.close_browser()
        
        mock_browser.close.assert_called_once()
        assert checker.browser is None

    def test_close_browser_no_browser(self, checker):
        """Test browser closure when no browser is running."""
        checker.browser = None
        
        # Should not raise exception
        checker.close_browser()


class TestCookieManagement:
    """Test cookie loading and management."""

    @pytest.fixture
    def mock_checker(self):
        """Create EmailChecker instance with mocked browser."""
        checker = EmailChecker()
        checker.browser = Mock()
        checker.page = Mock()
        return checker

    @patch('src.tavily_register.utils.helpers.load_cookies')
    def test_load_email_page_with_cookies(self, mock_load_cookies, mock_checker):
        """Test loading email page with saved cookies."""
        mock_load_cookies.return_value = SAMPLE_COOKIES
        mock_checker.page.context.add_cookies.return_value = None
        mock_checker.page.goto.return_value = None
        
        result = mock_checker.load_email_page()
        
        assert result is True
        mock_load_cookies.assert_called_once()
        mock_checker.page.context.add_cookies.assert_called_with(SAMPLE_COOKIES)
        mock_checker.page.goto.assert_called()

    @patch('src.tavily_register.utils.helpers.load_cookies')
    def test_load_email_page_no_cookies(self, mock_load_cookies, mock_checker):
        """Test loading email page when no cookies are available."""
        mock_load_cookies.return_value = None
        
        result = mock_checker.load_email_page()
        
        assert result is False

    @patch('src.tavily_register.utils.helpers.load_cookies')
    def test_load_email_page_cookie_error(self, mock_load_cookies, mock_checker):
        """Test loading email page when cookie loading fails."""
        mock_load_cookies.return_value = SAMPLE_COOKIES
        mock_checker.page.context.add_cookies.side_effect = Exception("Cookie error")
        
        result = mock_checker.load_email_page()
        
        assert result is False


class TestEmailDetection:
    """Test email detection and parsing functionality."""

    @pytest.fixture
    def mock_checker(self):
        """Create EmailChecker instance with mocked page."""
        checker = EmailChecker()
        checker.page = Mock()
        return checker

    def test_find_emails_on_page_success(self, mock_checker):
        """Test successful email detection on page."""
        # Mock email elements
        mock_email_elements = [
            Mock(inner_text=lambda: "From: noreply@tavily.com\nSubject: Verify your email"),
            Mock(inner_text=lambda: "From: support@tavily.com\nSubject: Welcome to Tavily")
        ]
        mock_checker.page.query_selector_all.return_value = mock_email_elements
        
        emails = mock_checker.find_emails_on_page()
        
        assert len(emails) == 2
        assert "noreply@tavily.com" in emails[0]['text']
        assert "support@tavily.com" in emails[1]['text']

    def test_find_emails_on_page_no_emails(self, mock_checker):
        """Test email detection when no emails are found."""
        mock_checker.page.query_selector_all.return_value = []
        
        emails = mock_checker.find_emails_on_page()
        
        assert emails == []

    def test_find_emails_on_page_error(self, mock_checker):
        """Test email detection with page error."""
        mock_checker.page.query_selector_all.side_effect = Exception("Page error")
        
        emails = mock_checker.find_emails_on_page()
        
        assert emails == []

    def test_parse_email_content_verification_email(self, mock_checker):
        """Test parsing verification email content."""
        email_text = "From: noreply@tavily.com\nSubject: Verify your email\nClick here: https://app.tavily.com/verify?token=abc123"
        
        parsed = mock_checker.parse_email_content(email_text)
        
        assert parsed['sender'] == "noreply@tavily.com"
        assert "verify" in parsed['subject'].lower()
        assert "https://app.tavily.com/verify?token=abc123" in parsed['links']

    def test_parse_email_content_no_links(self, mock_checker):
        """Test parsing email content with no links."""
        email_text = "From: support@tavily.com\nSubject: Welcome\nWelcome to our service!"
        
        parsed = mock_checker.parse_email_content(email_text)
        
        assert parsed['sender'] == "support@tavily.com"
        assert parsed['subject'] == "Welcome"
        assert parsed['links'] == []

    def test_parse_email_content_malformed(self, mock_checker):
        """Test parsing malformed email content."""
        email_text = "Invalid email format"
        
        parsed = mock_checker.parse_email_content(email_text)
        
        assert parsed['sender'] == ""
        assert parsed['subject'] == ""
        assert parsed['body'] == email_text


class TestVerificationLinkExtraction:
    """Test verification link extraction functionality."""

    @pytest.fixture
    def mock_checker(self):
        """Create EmailChecker instance for link extraction tests."""
        checker = EmailChecker()
        return checker

    def test_extract_verification_link_tavily(self, mock_checker):
        """Test extracting Tavily verification link."""
        email_content = "Please verify your email by clicking: https://app.tavily.com/verify?token=abc123def456"
        
        link = mock_checker.extract_verification_link(email_content)
        
        assert link == "https://app.tavily.com/verify?token=abc123def456"

    def test_extract_verification_link_multiple_links(self, mock_checker):
        """Test extracting verification link when multiple links are present."""
        email_content = """
        Visit our website: https://tavily.com
        Verify your email: https://app.tavily.com/verify?token=xyz789
        Unsubscribe: https://tavily.com/unsubscribe
        """
        
        link = mock_checker.extract_verification_link(email_content)
        
        assert link == "https://app.tavily.com/verify?token=xyz789"

    def test_extract_verification_link_no_verification_link(self, mock_checker):
        """Test extracting verification link when none exists."""
        email_content = "Welcome to Tavily! Visit us at https://tavily.com"
        
        link = mock_checker.extract_verification_link(email_content)
        
        assert link is None

    def test_extract_verification_link_malformed_url(self, mock_checker):
        """Test extracting verification link with malformed URL."""
        email_content = "Verify here: app.tavily.com/verify?token=invalid"
        
        link = mock_checker.extract_verification_link(email_content)
        
        assert link is None

    def test_extract_verification_link_different_patterns(self, mock_checker):
        """Test extracting verification links with different URL patterns."""
        test_cases = [
            "https://app.tavily.com/verify?token=abc123",
            "https://app.tavily.com/email/verify?code=def456",
            "https://app.tavily.com/confirm?verification=ghi789"
        ]
        
        for email_content in test_cases:
            link = mock_checker.extract_verification_link(f"Click here: {email_content}")
            assert link == email_content


class TestEmailWaiting:
    """Test email waiting and polling mechanisms."""

    @pytest.fixture
    def mock_checker(self):
        """Create EmailChecker instance with mocked methods."""
        checker = EmailChecker()
        checker.page = Mock()
        return checker

    @patch('time.sleep')
    def test_wait_for_email_success(self, mock_sleep, mock_checker):
        """Test successful email waiting."""
        # Mock finding verification email on second attempt
        mock_checker.find_emails_on_page.side_effect = [
            [],  # First attempt: no emails
            [{'text': 'From: noreply@tavily.com\nSubject: Verify\nhttps://app.tavily.com/verify?token=abc123'}]
        ]
        mock_checker.extract_verification_link.return_value = "https://app.tavily.com/verify?token=abc123"
        
        link = mock_checker.wait_for_email("test@2925.com", timeout=60)
        
        assert link == "https://app.tavily.com/verify?token=abc123"
        assert mock_checker.find_emails_on_page.call_count == 2
        mock_sleep.assert_called()

    @patch('time.sleep')
    def test_wait_for_email_timeout(self, mock_sleep, mock_checker):
        """Test email waiting timeout."""
        # Mock never finding the email
        mock_checker.find_emails_on_page.return_value = []
        
        link = mock_checker.wait_for_email("test@2925.com", timeout=5)
        
        assert link is None
        assert mock_checker.find_emails_on_page.call_count > 1

    @patch('time.sleep')
    def test_wait_for_email_wrong_recipient(self, mock_sleep, mock_checker):
        """Test email waiting for wrong recipient."""
        # Mock finding email for different recipient
        mock_checker.find_emails_on_page.return_value = [
            {'text': 'To: other@example.com\nFrom: noreply@tavily.com\nSubject: Verify'}
        ]
        
        link = mock_checker.wait_for_email("test@2925.com", timeout=5)
        
        assert link is None

    def test_wait_for_email_immediate_success(self, mock_checker):
        """Test email waiting with immediate success."""
        # Mock finding email immediately
        mock_checker.find_emails_on_page.return_value = [
            {'text': 'To: test@2925.com\nFrom: noreply@tavily.com\nSubject: Verify\nhttps://app.tavily.com/verify?token=abc123'}
        ]
        mock_checker.extract_verification_link.return_value = "https://app.tavily.com/verify?token=abc123"
        
        link = mock_checker.wait_for_email("test@2925.com", timeout=60)
        
        assert link == "https://app.tavily.com/verify?token=abc123"
        assert mock_checker.find_emails_on_page.call_count == 1


class TestErrorHandling:
    """Test error handling and edge cases."""

    @pytest.fixture
    def mock_checker(self):
        """Create EmailChecker instance for error testing."""
        checker = EmailChecker()
        checker.page = Mock()
        return checker

    def test_handle_page_load_error(self, mock_checker):
        """Test handling page load errors."""
        mock_checker.page.goto.side_effect = Exception("Page load failed")
        
        result = mock_checker.load_email_page()
        
        assert result is False

    def test_handle_email_parsing_error(self, mock_checker):
        """Test handling email parsing errors."""
        mock_checker.page.query_selector_all.side_effect = Exception("Parsing failed")
        
        emails = mock_checker.find_emails_on_page()
        
        assert emails == []

    def test_handle_browser_crash_during_wait(self, mock_checker):
        """Test handling browser crash during email waiting."""
        mock_checker.find_emails_on_page.side_effect = Exception("Browser crashed")
        
        link = mock_checker.wait_for_email("test@2925.com", timeout=5)
        
        assert link is None


class TestIntegrationScenarios:
    """Test integration scenarios and workflows."""

    @pytest.fixture
    def mock_checker(self):
        """Create EmailChecker instance for integration testing."""
        checker = EmailChecker()
        checker.browser = Mock()
        checker.page = Mock()
        return checker

    @patch('src.tavily_register.utils.helpers.load_cookies')
    def test_complete_email_verification_workflow(self, mock_load_cookies, mock_checker):
        """Test complete email verification workflow."""
        # Setup mocks for complete workflow
        mock_load_cookies.return_value = SAMPLE_COOKIES
        mock_checker.page.context.add_cookies.return_value = None
        mock_checker.page.goto.return_value = None
        
        # Mock finding verification email
        verification_email = get_sample_email_by_type("verification")
        mock_checker.find_emails_on_page.return_value = [
            {'text': f"To: test@2925.com\n{verification_email['body']}"}
        ]
        mock_checker.extract_verification_link.return_value = "https://app.tavily.com/verify?token=abc123"
        
        # Execute workflow
        load_result = mock_checker.load_email_page()
        verification_link = mock_checker.wait_for_email("test@2925.com", timeout=60)
        
        # Verify results
        assert load_result is True
        assert verification_link == "https://app.tavily.com/verify?token=abc123"

    def test_email_verification_with_retry(self, mock_checker):
        """Test email verification with retry mechanism."""
        # Mock initial failure, then success
        mock_checker.find_emails_on_page.side_effect = [
            [],  # First attempt: no emails
            [],  # Second attempt: still no emails
            [{'text': 'To: test@2925.com\nFrom: noreply@tavily.com\nhttps://app.tavily.com/verify?token=retry123'}]
        ]
        mock_checker.extract_verification_link.return_value = "https://app.tavily.com/verify?token=retry123"
        
        with patch('time.sleep'):
            link = mock_checker.wait_for_email("test@2925.com", timeout=30)
        
        assert link == "https://app.tavily.com/verify?token=retry123"
        assert mock_checker.find_emails_on_page.call_count == 3
