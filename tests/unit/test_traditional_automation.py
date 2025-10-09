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


class TestNavigationAndFormFilling:
    """Test navigation and form-filling methods."""

    def test_navigate_to_signup_success(self, automation: TavilyAutomation, mocker):
        """Test successful navigation to signup page."""
        mocker.patch.object(automation.page, 'goto')
        mocker.patch.object(automation.page, 'wait_for_selector', return_value=Mock())
        mocker.patch.object(automation.page, 'wait_for_load_state')

        result = automation.navigate_to_signup()

        assert result is True
        automation.page.goto.assert_called()

    def test_fill_registration_form_success(self, automation: TavilyAutomation, mocker):
        """Test successful registration form filling."""
        mock_email_input = Mock()
        mock_next_button = Mock()
        mocker.patch.object(
            automation.page,
            'wait_for_selector',
            side_effect=[mock_email_input, mock_next_button]
        )

        result = automation.fill_registration_form()

        assert result is True
        assert mock_email_input.fill.call_count == 1
        assert mock_next_button.click.call_count == 1

    def test_fill_password_success(self, automation: TavilyAutomation, mocker):
        """Test successful password filling."""
        mock_password_input = Mock()
        mock_confirm_input = Mock()  # Mock for the confirmation password field
        mock_submit_button = Mock()
        mocker.patch.object(
            automation.page,
            'wait_for_selector',
            side_effect=[
                mock_password_input,
                mock_confirm_input,
                mock_submit_button
            ]
        )

        result = automation.fill_password()

        assert result is True
        mock_password_input.fill.assert_called_with(automation.password)
        mock_confirm_input.fill.assert_called_with(automation.password)
        mock_submit_button.click.assert_called_once()


class TestErrorHandling:
    """Test error handling and recovery mechanisms."""

    def test_navigate_to_signup_failure(self, automation: TavilyAutomation, mocker):
        """Test navigation failure to signup page."""
        mocker.patch.object(automation.page, 'goto', side_effect=Exception("Navigation failed"))

        result = automation.navigate_to_signup()

        assert result is False

    def test_fill_registration_form_email_not_found(self, automation: TavilyAutomation, mocker):
        """Test form filling when email input is not found."""
        mocker.patch.object(
            automation.page,
            'wait_for_selector',
            side_effect=PlaywrightTimeoutError("Email input not found")
        )

        result = automation.fill_registration_form()

        assert result is False