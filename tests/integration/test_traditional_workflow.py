"""
Integration tests for the traditional automation workflow (Test Mode).
"""
import pytest
from unittest.mock import Mock, patch
from src.tavily_register.core.traditional_automation import TavilyAutomation

class TestTraditionalWorkflow:
    """Tests for the TavilyAutomation class and its registration workflow."""

    @pytest.fixture
    def mock_traditional_automation(self):
        """Create a mock TavilyAutomation instance for testing."""
        with patch('src.tavily_register.core.traditional_automation.sync_playwright') as mock_playwright:
            automation = TavilyAutomation()
            automation.page = Mock()
            automation.email_prefix = "test"
            yield automation

    def test_run_registration_success(self, mock_traditional_automation):
        """
        Test the run_registration method for a successful registration scenario.
        """
        automation = mock_traditional_automation

        # Mock the individual steps to return True
        with patch.object(automation, 'navigate_to_signup', return_value=True) as mock_navigate, \
             patch.object(automation, 'fill_registration_form', return_value=True) as mock_fill_form, \
             patch.object(automation, 'fill_password', return_value=True) as mock_fill_password:

            # Execute the registration process
            result = automation.run_registration()

            # Assert that the process was successful and all methods were called
            assert result is True
            mock_navigate.assert_called_once()
            mock_fill_form.assert_called_once()
            mock_fill_password.assert_called_once()

    def test_run_registration_failure_on_navigate(self, mock_traditional_automation):
        """
        Test the run_registration method for a failure during navigation.
        """
        automation = mock_traditional_automation

        # Mock navigation to fail
        with patch.object(automation, 'navigate_to_signup', return_value=False) as mock_navigate, \
             patch.object(automation, 'fill_registration_form') as mock_fill_form, \
             patch.object(automation, 'fill_password') as mock_fill_password:

            # Execute the registration process
            result = automation.run_registration()

            # Assert that the process failed and subsequent steps were not called
            assert result is False
            mock_navigate.assert_called_once()
            mock_fill_form.assert_not_called()
            mock_fill_password.assert_not_called()

    def test_run_registration_failure_on_fill_form(self, mock_traditional_automation):
        """
        Test the run_registration method for a failure during form filling.
        """
        automation = mock_traditional_automation

        # Mock form filling to fail
        with patch.object(automation, 'navigate_to_signup', return_value=True) as mock_navigate, \
             patch.object(automation, 'fill_registration_form', return_value=False) as mock_fill_form, \
             patch.object(automation, 'fill_password') as mock_fill_password:

            # Execute the registration process
            result = automation.run_registration()

            # Assert that the process failed and the final step was not called
            assert result is False
            mock_navigate.assert_called_once()
            mock_fill_form.assert_called_once()
            mock_fill_password.assert_not_called()