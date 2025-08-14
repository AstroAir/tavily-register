"""
Comprehensive unit tests for TavilyMainController class.

Tests the main application controller including menu system,
workflow orchestration, configuration management, and user interaction.
"""
import pytest
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock, call
from io import StringIO

from src.tavily_register.main import TavilyMainController
from tests.fixtures.sample_data import (
    SAMPLE_CONFIGS,
    SAMPLE_AUTOMATION_RESULTS
)


class TestTavilyMainControllerInit:
    """Test TavilyMainController initialization and setup."""

    def test_initialization_default_values(self):
        """Test controller instance initialization with default values."""
        controller = TavilyMainController()
        
        assert controller.email_prefix is None
        assert controller.cookie_file == "email_cookies.json"

    def test_initialization_attributes(self):
        """Test controller has required attributes."""
        controller = TavilyMainController()
        
        assert hasattr(controller, 'email_prefix')
        assert hasattr(controller, 'cookie_file')


class TestMenuSystem:
    """Test menu system and user interface."""

    @pytest.fixture
    def controller(self):
        """Create controller instance for testing."""
        return TavilyMainController()

    @patch('builtins.print')
    @patch('builtins.input')
    def test_show_main_menu_display(self, mock_input, mock_print, controller):
        """Test main menu display."""
        mock_input.return_value = "4"  # Exit option
        
        choice = controller.show_main_menu()
        
        assert choice == "4"
        # Should print menu options
        assert mock_print.call_count > 0
        
        # Check that menu contains expected options
        printed_text = " ".join([str(call.args[0]) for call in mock_print.call_args_list])
        assert "智能注册模式" in printed_text or "intelligent" in printed_text.lower()

    @patch('builtins.input')
    def test_show_main_menu_user_choices(self, mock_input, controller):
        """Test main menu handles different user choices."""
        test_choices = ["1", "2", "3", "4", "invalid"]
        
        for choice in test_choices:
            mock_input.return_value = choice
            result = controller.show_main_menu()
            assert result == choice

    @patch('builtins.print')
    def test_menu_formatting(self, mock_print, controller):
        """Test menu formatting and presentation."""
        with patch('builtins.input', return_value="4"):
            controller.show_main_menu()
        
        # Should have proper formatting with separators
        printed_calls = [str(call.args[0]) for call in mock_print.call_args_list]
        has_separators = any("=" in call for call in printed_calls)
        assert has_separators


class TestConfigurationManagement:
    """Test configuration and setup management."""

    @pytest.fixture
    def controller(self):
        """Create controller instance for testing."""
        return TavilyMainController()

    @patch('src.tavily_register.utils.helpers.load_cookies')
    def test_get_email_prefix_from_cookies_success(self, mock_load_cookies, controller):
        """Test successful email prefix extraction from cookies."""
        mock_cookies = [
            {"name": "aut", "value": "eyJuYW1lIjoidGVzdEAyOTI1LmNvbSJ9"}  # Base64 encoded JSON
        ]
        mock_load_cookies.return_value = mock_cookies
        
        with patch('base64.b64decode') as mock_b64decode, \
             patch('json.loads') as mock_json_loads:
            mock_b64decode.return_value = b'{"name":"test@2925.com"}'
            mock_json_loads.return_value = {"name": "test@2925.com"}
            
            prefix = controller.get_email_prefix_from_cookies()
            
            assert prefix == "test"

    @patch('src.tavily_register.utils.helpers.load_cookies')
    def test_get_email_prefix_from_cookies_no_cookies(self, mock_load_cookies, controller):
        """Test email prefix extraction when no cookies exist."""
        mock_load_cookies.return_value = None
        
        prefix = controller.get_email_prefix_from_cookies()
        
        assert prefix is None

    @patch('src.tavily_register.utils.helpers.load_cookies')
    def test_get_email_prefix_from_cookies_invalid_format(self, mock_load_cookies, controller):
        """Test email prefix extraction with invalid cookie format."""
        mock_cookies = [{"name": "aut", "value": "invalid_base64"}]
        mock_load_cookies.return_value = mock_cookies
        
        prefix = controller.get_email_prefix_from_cookies()
        
        assert prefix is None

    @patch('builtins.input')
    def test_get_run_config_default(self, mock_input, controller):
        """Test getting run configuration with defaults."""
        mock_input.side_effect = ["", ""]  # Use defaults
        
        headless, count = controller.get_run_config()
        
        assert isinstance(headless, bool)
        assert isinstance(count, int)
        assert count > 0

    @patch('builtins.input')
    def test_get_run_config_custom_values(self, mock_input, controller):
        """Test getting run configuration with custom values."""
        mock_input.side_effect = ["n", "5"]  # Not headless, 5 accounts
        
        headless, count = controller.get_run_config()
        
        assert headless is False
        assert count == 5

    @patch('builtins.input')
    def test_get_run_config_invalid_input(self, mock_input, controller):
        """Test getting run configuration with invalid input."""
        mock_input.side_effect = ["invalid", "not_a_number", "", ""]  # Invalid then defaults
        
        headless, count = controller.get_run_config()
        
        # Should handle invalid input gracefully and use defaults
        assert isinstance(headless, bool)
        assert isinstance(count, int)


class TestEmailSetup:
    """Test email setup and cookie management."""

    @pytest.fixture
    def controller(self):
        """Create controller instance for testing."""
        return TavilyMainController()

    @patch('src.tavily_register.email.login_helper.EmailLoginHelper')
    def test_setup_email_cookies_success(self, mock_helper_class, controller):
        """Test successful email cookie setup."""
        mock_helper = Mock()
        mock_helper_class.return_value = mock_helper
        mock_helper.start_browser.return_value = None
        mock_helper.interactive_email_setup.return_value = True
        mock_helper.close_browser.return_value = None
        
        controller.setup_email_cookies()
        
        mock_helper.start_browser.assert_called_once()
        mock_helper.interactive_email_setup.assert_called_once()
        mock_helper.close_browser.assert_called_once()

    @patch('src.tavily_register.email.login_helper.EmailLoginHelper')
    def test_setup_email_cookies_failure(self, mock_helper_class, controller):
        """Test email cookie setup failure."""
        mock_helper = Mock()
        mock_helper_class.return_value = mock_helper
        mock_helper.start_browser.side_effect = Exception("Browser failed")
        
        # Should handle exception gracefully
        controller.setup_email_cookies()
        
        mock_helper.start_browser.assert_called_once()

    @patch('src.tavily_register.email.login_helper.EmailLoginHelper')
    def test_setup_email_cookies_cleanup_on_error(self, mock_helper_class, controller):
        """Test email cookie setup cleanup on error."""
        mock_helper = Mock()
        mock_helper_class.return_value = mock_helper
        mock_helper.interactive_email_setup.side_effect = Exception("Setup failed")
        
        controller.setup_email_cookies()
        
        # Should still call close_browser for cleanup
        mock_helper.close_browser.assert_called_once()

    def test_check_and_setup_cookies_with_existing_prefix(self, controller):
        """Test cookie check when prefix already exists."""
        controller.email_prefix = "existing_prefix"
        
        result = controller.check_and_setup_cookies()
        
        assert result is True

    @patch('builtins.input')
    def test_check_and_setup_cookies_user_provides_prefix(self, mock_input, controller):
        """Test cookie check when user provides prefix."""
        mock_input.return_value = "user_prefix"
        controller.email_prefix = None
        
        result = controller.check_and_setup_cookies()
        
        assert result is True
        assert controller.email_prefix == "user_prefix"

    @patch('builtins.input')
    def test_check_and_setup_cookies_user_cancels(self, mock_input, controller):
        """Test cookie check when user cancels setup."""
        mock_input.side_effect = ["", "n"]  # No prefix, don't setup
        controller.email_prefix = None
        
        result = controller.check_and_setup_cookies()
        
        assert result is False


class TestIntelligentMode:
    """Test intelligent automation mode."""

    @pytest.fixture
    def controller(self):
        """Create controller instance for testing."""
        controller = TavilyMainController()
        controller.email_prefix = "test_prefix"
        return controller

    @patch('builtins.input')
    @patch('src.tavily_register.core.intelligent_automation.IntelligentTavilyAutomation')
    def test_run_intelligent_mode_success(self, mock_automation_class, mock_input, controller):
        """Test successful intelligent mode execution."""
        # Mock user confirmation
        mock_input.return_value = "y"
        
        # Mock automation
        mock_automation = Mock()
        mock_automation_class.return_value = mock_automation
        mock_automation.start_browser.return_value = None
        mock_automation.run_complete_automation.return_value = "tvly-dev-test123"
        mock_automation.email = "test@2925.com"
        mock_automation.close_browser.return_value = None
        
        # Mock configuration methods
        controller.check_and_setup_cookies = Mock(return_value=True)
        controller.get_run_config = Mock(return_value=(True, 1))
        
        controller.run_intelligent_mode()
        
        mock_automation.start_browser.assert_called()
        mock_automation.run_complete_automation.assert_called()
        mock_automation.close_browser.assert_called()

    @patch('builtins.input')
    def test_run_intelligent_mode_user_cancels(self, mock_input, controller):
        """Test intelligent mode when user cancels."""
        mock_input.return_value = "n"
        controller.check_and_setup_cookies = Mock(return_value=True)
        controller.get_run_config = Mock(return_value=(True, 1))
        
        with patch('builtins.print') as mock_print:
            controller.run_intelligent_mode()
            
            # Should print cancellation message
            printed_text = " ".join([str(call.args[0]) for call in mock_print.call_args_list])
            assert "取消" in printed_text or "cancel" in printed_text.lower()

    @patch('builtins.input')
    @patch('src.tavily_register.core.intelligent_automation.IntelligentTavilyAutomation')
    def test_run_intelligent_mode_automation_failure(self, mock_automation_class, mock_input, controller):
        """Test intelligent mode with automation failure."""
        mock_input.return_value = "y"
        
        mock_automation = Mock()
        mock_automation_class.return_value = mock_automation
        mock_automation.start_browser.return_value = None
        mock_automation.run_complete_automation.return_value = None  # Failure
        mock_automation.close_browser.return_value = None
        
        controller.check_and_setup_cookies = Mock(return_value=True)
        controller.get_run_config = Mock(return_value=(True, 1))
        
        controller.run_intelligent_mode()
        
        # Should still clean up properly
        mock_automation.close_browser.assert_called()

    def test_run_intelligent_mode_setup_failure(self, controller):
        """Test intelligent mode with setup failure."""
        controller.check_and_setup_cookies = Mock(return_value=False)
        
        with patch('builtins.print') as mock_print:
            controller.run_intelligent_mode()
            
            # Should print error message
            printed_text = " ".join([str(call.args[0]) for call in mock_print.call_args_list])
            assert "失败" in printed_text or "fail" in printed_text.lower()


class TestTestMode:
    """Test traditional automation test mode."""

    @pytest.fixture
    def controller(self):
        """Create controller instance for testing."""
        controller = TavilyMainController()
        controller.email_prefix = "test_prefix"
        return controller

    @patch('builtins.input')
    @patch('src.tavily_register.core.traditional_automation.TavilyAutomation')
    def test_run_test_mode_success(self, mock_automation_class, mock_input, controller):
        """Test successful test mode execution."""
        mock_input.return_value = "y"
        
        mock_automation = Mock()
        mock_automation_class.return_value = mock_automation
        mock_automation.start_browser.return_value = None
        mock_automation.navigate_to_signup.return_value = True
        mock_automation.save_html_log.return_value = None
        mock_automation.close_browser.return_value = None
        
        controller.check_and_setup_cookies = Mock(return_value=True)
        controller.get_run_config = Mock(return_value=(True, 1))
        
        controller.run_test_mode()
        
        mock_automation.start_browser.assert_called()
        mock_automation.navigate_to_signup.assert_called()
        mock_automation.save_html_log.assert_called()
        mock_automation.close_browser.assert_called()

    @patch('builtins.input')
    def test_run_test_mode_user_cancels(self, mock_input, controller):
        """Test test mode when user cancels."""
        mock_input.return_value = "n"
        controller.check_and_setup_cookies = Mock(return_value=True)
        controller.get_run_config = Mock(return_value=(True, 1))
        
        with patch('builtins.print') as mock_print:
            controller.run_test_mode()
            
            printed_text = " ".join([str(call.args[0]) for call in mock_print.call_args_list])
            assert "取消" in printed_text or "cancel" in printed_text.lower()

    def test_run_test_mode_setup_failure(self, controller):
        """Test test mode with setup failure."""
        controller.check_and_setup_cookies = Mock(return_value=False)
        
        with patch('builtins.print') as mock_print:
            controller.run_test_mode()
            
            printed_text = " ".join([str(call.args[0]) for call in mock_print.call_args_list])
            assert "失败" in printed_text or "fail" in printed_text.lower()


class TestMainRunLoop:
    """Test main application run loop."""

    @pytest.fixture
    def controller(self):
        """Create controller instance for testing."""
        return TavilyMainController()

    @patch('builtins.input')
    def test_run_exit_immediately(self, mock_input, controller):
        """Test run loop exits immediately when user chooses exit."""
        mock_input.return_value = "4"  # Exit option
        controller.show_main_menu = Mock(return_value="4")
        
        controller.run()
        
        controller.show_main_menu.assert_called_once()

    @patch('builtins.input')
    def test_run_invalid_choice(self, mock_input, controller):
        """Test run loop handles invalid menu choices."""
        controller.show_main_menu = Mock(side_effect=["invalid", "4"])
        
        with patch('builtins.print') as mock_print:
            controller.run()
            
            # Should print error message for invalid choice
            printed_text = " ".join([str(call.args[0]) for call in mock_print.call_args_list])
            assert "无效" in printed_text or "invalid" in printed_text.lower()

    @patch('builtins.input')
    def test_run_continue_after_operation(self, mock_input, controller):
        """Test run loop continues after operation."""
        mock_input.side_effect = ["y", "n"]  # Continue, then exit
        controller.show_main_menu = Mock(side_effect=["1", "4"])
        controller.run_intelligent_mode = Mock()
        
        controller.run()
        
        assert controller.show_main_menu.call_count == 2
        controller.run_intelligent_mode.assert_called_once()


class TestErrorHandling:
    """Test error handling and edge cases."""

    @pytest.fixture
    def controller(self):
        """Create controller instance for error testing."""
        return TavilyMainController()

    def test_handle_missing_email_prefix(self, controller):
        """Test handling when email prefix is missing."""
        controller.email_prefix = None
        
        result = controller.check_and_setup_cookies()
        
        # Should handle gracefully
        assert isinstance(result, bool)

    @patch('src.tavily_register.utils.helpers.load_cookies')
    def test_handle_corrupted_cookies(self, mock_load_cookies, controller):
        """Test handling corrupted cookie data."""
        mock_load_cookies.side_effect = Exception("Corrupted cookies")
        
        prefix = controller.get_email_prefix_from_cookies()
        
        assert prefix is None

    @patch('builtins.input')
    def test_handle_user_interrupt(self, mock_input, controller):
        """Test handling user interrupt (Ctrl+C)."""
        mock_input.side_effect = KeyboardInterrupt()
        
        # Should handle KeyboardInterrupt gracefully
        try:
            controller.show_main_menu()
        except KeyboardInterrupt:
            pass  # Expected behavior

    def test_handle_automation_exception(self, controller):
        """Test handling automation exceptions."""
        controller.email_prefix = "test"
        controller.check_and_setup_cookies = Mock(return_value=True)
        controller.get_run_config = Mock(return_value=(True, 1))
        
        with patch('src.tavily_register.core.intelligent_automation.IntelligentTavilyAutomation') as mock_class:
            mock_class.side_effect = Exception("Automation failed")
            
            with patch('builtins.input', return_value="y"):
                # Should handle exception gracefully
                controller.run_intelligent_mode()


class TestIntegrationScenarios:
    """Test integration scenarios and complete workflows."""

    @pytest.fixture
    def controller(self):
        """Create controller instance for integration testing."""
        return TavilyMainController()

    @patch('builtins.input')
    def test_complete_workflow_simulation(self, mock_input, controller):
        """Test complete workflow from menu to completion."""
        # Simulate user choosing intelligent mode, confirming, then exiting
        mock_input.side_effect = ["1", "y", "n"]
        
        # Mock all dependencies
        controller.check_and_setup_cookies = Mock(return_value=True)
        controller.get_run_config = Mock(return_value=(True, 1))
        
        with patch('src.tavily_register.core.intelligent_automation.IntelligentTavilyAutomation') as mock_automation_class:
            mock_automation = Mock()
            mock_automation_class.return_value = mock_automation
            mock_automation.run_complete_automation.return_value = "tvly-dev-test123"
            mock_automation.email = "test@2925.com"
            
            controller.run()
            
            # Verify complete workflow executed
            mock_automation.start_browser.assert_called()
            mock_automation.run_complete_automation.assert_called()
            mock_automation.close_browser.assert_called()

    def test_configuration_persistence(self, controller):
        """Test configuration persistence across operations."""
        controller.email_prefix = "persistent_test"
        
        # Email prefix should persist across different operations
        assert controller.email_prefix == "persistent_test"
        
        # Should be available for automation instances
        controller.check_and_setup_cookies = Mock(return_value=True)
        result = controller.check_and_setup_cookies()
        assert result is True
