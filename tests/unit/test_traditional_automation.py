"""
Comprehensive unit tests for TavilyAutomation class.

Tests the traditional automation module including browser lifecycle,
HTML collection, element detection, and fallback mechanisms.
"""
import pytest
from unittest.mock import Mock, patch
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from src.tavily_register.core.traditional_automation import TavilyAutomation

@pytest.fixture
def automation(page: Page) -> TavilyAutomation:
    """Provides a TavilyAutomation instance with a page fixture."""
    return TavilyAutomation(page=page)


class TestTavilyAutomationInit:
    """Test initialization and basic setup."""

    def test_initialization_with_page(self, page: Page):
        """Test initialization with a page object."""
        automation = TavilyAutomation(page=page)
        assert automation.page == page
        assert automation._own_browser is False

    def test_initialization_without_page(self):
        """Test initialization without a page object (will manage its own browser)."""
        automation = TavilyAutomation()
        assert automation.page is None
        assert automation._own_browser is True
        assert hasattr(automation, 'playwright')
        assert hasattr(automation, 'browser')


class TestBrowserLifecycle:
    """Test browser lifecycle management for traditional automation."""

    def test_start_browser_if_own_browser(self):
        """Test that start_browser only runs if the instance owns the browser."""
        with patch('playwright.sync_api.sync_playwright') as mock_playwright:
            mock_playwright_instance = Mock()
            mock_browser = Mock()
            mock_page = Mock()
            mock_playwright.return_value.start.return_value = mock_playwright_instance
            mock_playwright_instance.firefox.launch.return_value = mock_browser
            mock_browser.new_page.return_value = mock_page

            automation = TavilyAutomation()  # Owns browser
            automation.start_browser(headless=True)

            mock_playwright_instance.firefox.launch.assert_called_once_with(headless=True)
            assert automation.page is not None

    def test_start_browser_if_not_own_browser(self, automation: TavilyAutomation):
        """Test that start_browser does nothing if a page is provided."""
        with patch('playwright.sync_api.sync_playwright') as mock_playwright:
            automation.start_browser()
            mock_playwright.return_value.start.assert_not_called()

    def test_close_browser_if_own_browser(self):
        """Test that close_browser only runs if the instance owns the browser."""
        with patch('playwright.sync_api.sync_playwright'):
            automation = TavilyAutomation()
            automation.playwright = Mock()
            automation.browser = Mock()
            automation.page = Mock()

            automation.close_browser()

            automation.page.close.assert_called_once()
            automation.browser.close.assert_called_once()
            automation.playwright.stop.assert_called_once()

    def test_close_browser_if_not_own_browser(self, automation: TavilyAutomation):
        """Test that close_browser does nothing if a page is provided."""
        page = automation.page
        page.close = Mock()
        automation.close_browser()
        page.close.assert_not_called()

class TestNavigationAndFormFilling:
    """Test navigation and form-filling methods."""

    def test_navigate_to_signup_success(self, automation: TavilyAutomation):
        """Test successful navigation to signup page."""
        automation.page.goto = Mock()
        automation.page.wait_for_selector = Mock(return_value=Mock())
        automation.page.wait_for_load_state = Mock()

        result = automation.navigate_to_signup()

        assert result is True
        automation.page.goto.assert_called()

    def test_fill_registration_form_success(self, automation: TavilyAutomation):
        """Test successful registration form filling."""
        mock_email_input = Mock()
        mock_next_button = Mock()
        automation.page.wait_for_selector.side_effect = [
            mock_email_input,
            mock_next_button,
        ]
        
        result = automation.fill_registration_form()

        assert result is True
        assert mock_email_input.fill.call_count == 1
        assert mock_next_button.click.call_count == 1

    def test_fill_password_success(self, automation: TavilyAutomation):
        """Test successful password filling."""
        mock_password_input = Mock()
        mock_submit_button = Mock()
        automation.page.wait_for_selector.side_effect = [
            mock_password_input,
            mock_submit_button
        ]

        result = automation.fill_password()

        assert result is True
        mock_password_input.fill.assert_called_with(automation.password)
        mock_submit_button.click.assert_called_once()


class TestErrorHandling:
    """Test error handling and recovery mechanisms."""

    def test_navigate_to_signup_failure(self, automation: TavilyAutomation):
        """Test navigation failure to signup page."""
        automation.page.goto.side_effect = Exception("Navigation failed")
        
        result = automation.navigate_to_signup()
        
        assert result is False

    def test_fill_registration_form_email_not_found(self, automation: TavilyAutomation):
        """Test form filling when email input is not found."""
        automation.page.wait_for_selector.side_effect = PlaywrightTimeoutError("Email input not found")
        
        result = automation.fill_registration_form()
        
        assert result is False