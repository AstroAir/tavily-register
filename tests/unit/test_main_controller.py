"""
Comprehensive unit tests for TavilyMainController class.

Tests the main application controller including menu system,
workflow orchestration, configuration management, and user interaction.
"""
import pytest
from unittest.mock import Mock, patch
from src.tavily_register.main import TavilyMainController


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
    @patch('builtins.input', return_value="4")
    def test_show_main_menu_display(self, mock_input, mock_print, controller):
        """Test main menu display."""
        choice = controller.show_main_menu()
        assert choice == "4"
        assert mock_print.call_count > 0
        printed_text = " ".join([str(call.args[0]) for call in mock_print.call_args_list])
        assert "智能自动化模式" in printed_text or "intelligent" in printed_text.lower()

    @patch('builtins.input')
    def test_show_main_menu_user_choices(self, mock_input, controller):
        """Test main menu handles different user choices."""
        for choice in ["1", "2", "3", "4", "invalid"]:
            mock_input.return_value = choice
            assert controller.show_main_menu() == choice

    @patch('builtins.print')
    def test_menu_formatting(self, mock_print, controller):
        """Test menu formatting and presentation."""
        with patch('builtins.input', return_value="4"):
            controller.show_main_menu()
        printed_calls = [str(call.args[0]) for call in mock_print.call_args_list]
        assert any("=" in call for call in printed_calls)


class TestConfigurationManagement:
    """Test configuration and setup management."""

    @pytest.fixture
    def controller(self):
        """Create controller instance for testing."""
        return TavilyMainController()

    @patch('src.tavily_register.main.load_cookies')
    def test_get_email_prefix_from_cookies_success(self, mock_load_cookies, controller):
        """Test successful email prefix extraction from cookies."""
        # Mock a JWT-like structure with a dummy header and signature
        mock_cookies = [{"name": "aut", "value": "a.eyJuYW1lIjoidGVzdEAyOTI1LmNvbSJ9.b"}]
        mock_load_cookies.return_value = mock_cookies
        with patch('base64.urlsafe_b64decode', return_value=b'{"name":"test@2925.com"}'):
            prefix = controller.get_email_prefix_from_cookies()
            assert prefix == "test"

    @patch('src.tavily_register.main.load_cookies', return_value=None)
    def test_get_email_prefix_from_cookies_no_cookies(self, mock_load_cookies, controller):
        """Test email prefix extraction when no cookies exist."""
        assert controller.get_email_prefix_from_cookies() is None

    @patch('src.tavily_register.main.load_cookies')
    def test_get_email_prefix_from_cookies_invalid_format(self, mock_load_cookies, controller):
        """Test email prefix extraction with invalid cookie format."""
        mock_load_cookies.return_value = [{"name": "aut", "value": "invalid_base64"}]
        with patch('base64.urlsafe_b64decode', side_effect=Exception("decoding failed")):
            assert controller.get_email_prefix_from_cookies() is None

    @patch('builtins.input', side_effect=["1", "5"])
    def test_get_run_config_custom_values(self, mock_input, controller):
        """Test getting run configuration with custom values."""
        headless, count = controller.get_run_config()
        assert headless is False
        assert count == 5


class TestEmailSetup:
    """Test email setup and cookie management."""

    @pytest.fixture
    def controller(self):
        """Create controller instance for testing."""
        return TavilyMainController()

    @patch('src.tavily_register.main.sync_playwright')
    @patch('src.tavily_register.main.EmailLoginHelper')
    def test_setup_email_cookies_success(self, mock_helper_class, mock_playwright, controller):
        """Test successful email cookie setup."""
        mock_page = Mock()
        mock_browser = Mock()
        mock_playwright_context = mock_playwright.return_value.__enter__.return_value
        mock_playwright_context.chromium.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page
        mock_helper_class.return_value.interactive_email_setup.return_value = True
        controller.get_email_prefix_from_cookies = Mock(return_value="test_prefix")

        assert controller.setup_email_cookies() is True
        mock_helper_class.assert_called_once_with(mock_page)
        mock_helper_class.return_value.interactive_email_setup.assert_called_once()
        mock_browser.close.assert_called_once()

    @patch('src.tavily_register.main.sync_playwright', side_effect=Exception("Setup failed"))
    def test_setup_email_cookies_failure(self, mock_playwright, controller):
        """Test email cookie setup failure."""
        assert controller.setup_email_cookies() is False

class TestIntelligentMode:
    """Test intelligent automation mode."""

    @pytest.fixture
    def controller(self):
        """Create controller instance for testing."""
        controller = TavilyMainController()
        controller.email_prefix = "test_prefix"
        return controller

    @patch('builtins.input', return_value='y')
    @patch('src.tavily_register.main.sync_playwright')
    @patch('src.tavily_register.main.IntelligentTavilyAutomation')
    def test_run_intelligent_mode_success(self, mock_automation_class, mock_playwright, mock_input, controller):
        """Test successful intelligent mode execution."""
        mock_page = Mock()
        mock_context = Mock()
        mock_browser = Mock()
        mock_playwright_context = mock_playwright.return_value.__enter__.return_value
        mock_playwright_context.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_automation_class.return_value.run_complete_automation.return_value = "tvly-dev-test123"
        controller.check_and_setup_cookies = Mock(return_value=True)
        controller.get_run_config = Mock(return_value=(True, 1))

        controller.run_intelligent_mode()

        mock_automation_class.assert_called_once_with(mock_page)
        mock_automation_class.return_value.run_complete_automation.assert_called_once()
        mock_context.close.assert_called_once()
        mock_browser.close.assert_called_once()

class TestTestMode:
    """Test traditional automation test mode."""

    @pytest.fixture
    def controller(self):
        """Create controller instance for testing."""
        controller = TavilyMainController()
        controller.email_prefix = "test_prefix"
        return controller

    @patch('builtins.input', return_value='y')
    @patch('src.tavily_register.main.sync_playwright')
    @patch('src.tavily_register.main.TavilyAutomation')
    def test_run_test_mode_success(self, mock_automation_class, mock_playwright, mock_input, controller):
        """Test successful test mode execution."""
        mock_page = Mock()
        mock_context = Mock()
        mock_browser = Mock()
        mock_playwright_context = mock_playwright.return_value.__enter__.return_value
        mock_playwright_context.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_automation_class.return_value.run_registration.return_value = True
        controller.check_and_setup_cookies = Mock(return_value=True)
        controller.get_run_config = Mock(return_value=(True, 1))

        controller.run_test_mode()

        mock_automation_class.assert_called_once_with(mock_page)
        mock_automation_class.return_value.run_registration.assert_called_once()
        mock_context.close.assert_called_once()
        mock_browser.close.assert_called_once()

class TestMainRunLoop:
    """Test main application run loop."""

    @pytest.fixture
    def controller(self):
        """Create controller instance for testing."""
        return TavilyMainController()

    @patch('builtins.input', return_value="4")
    def test_run_exit_immediately(self, mock_input, controller):
        """Test run loop exits immediately when user chooses exit."""
        controller.run()
        mock_input.assert_called_once()

class TestErrorHandling:
    """Test error handling and edge cases."""

    @pytest.fixture
    def controller(self):
        """Create controller instance for error testing."""
        return TavilyMainController()

    @patch('src.tavily_register.main.load_cookies', side_effect=Exception("Corrupted cookies"))
    def test_handle_corrupted_cookies(self, mock_load_cookies, controller):
        """Test handling corrupted cookie data."""
        assert controller.get_email_prefix_from_cookies() is None

class TestIntegrationScenarios:
    """Test integration scenarios and complete workflows."""

    @pytest.fixture
    def controller(self):
        """Create controller instance for integration testing."""
        return TavilyMainController()

    @patch('builtins.input', side_effect=["1", "y", "n"])
    @patch('src.tavily_register.main.sync_playwright')
    @patch('src.tavily_register.main.IntelligentTavilyAutomation')
    def test_complete_workflow_simulation(self, mock_automation_class, mock_playwright, mock_input, controller):
        """Test complete workflow from menu to completion."""
        controller.check_and_setup_cookies = Mock(return_value=True)
        controller.get_run_config = Mock(return_value=(True, 1))

        mock_page = Mock()
        mock_context = Mock()
        mock_browser = Mock()
        mock_playwright_context = mock_playwright.return_value.__enter__.return_value
        mock_playwright_context.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        mock_automation_class.return_value.run_complete_automation.return_value = "tvly-dev-test123"

        controller.run()
        
        mock_automation_class.assert_called_once_with(mock_page)
        mock_automation_class.return_value.run_complete_automation.assert_called_once()