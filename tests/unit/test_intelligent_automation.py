"""
Unit tests for the IntelligentTavilyAutomation class.
"""
import pytest
from unittest.mock import Mock, patch
from playwright.sync_api import Page
from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation

@pytest.fixture
def automation_with_page(mocker):
    """Provides an IntelligentTavilyAutomation instance with a mocked page."""
    mock_page = mocker.MagicMock(spec=Page)
    return IntelligentTavilyAutomation(page=mock_page)

@pytest.fixture
def automation_without_page():
    """Provides an IntelligentTavilyAutomation instance without a page."""
    return IntelligentTavilyAutomation()

class TestIntelligentTavilyAutomationInit:
    """Tests for the initialization of IntelligentTavilyAutomation."""

    def test_initialization_with_page(self, automation_with_page):
        """Test initialization with a provided page."""
        assert automation_with_page.page is not None
        assert automation_with_page._own_browser is False

    def test_initialization_without_page(self, automation_without_page):
        """Test initialization without a provided page."""
        assert automation_without_page.page is None
        assert automation_without_page._own_browser is True
        assert automation_without_page.playwright is None
        assert automation_without_page.browser is None

class TestLogging:
    """Tests for the logging functionality."""

    def test_log_enabled(self, capsys):
        """Test that log messages are printed when debugging is enabled."""
        automation = IntelligentTavilyAutomation()
        automation.debug = True
        automation.log("Test message")
        captured = capsys.readouterr()
        assert "Test message" in captured.out

    def test_log_disabled(self, capsys):
        """Test that log messages are not printed when debugging is disabled."""
        automation = IntelligentTavilyAutomation()
        automation.debug = False
        automation.log("Test message")
        captured = capsys.readouterr()
        assert captured.out == ""

class TestBrowserLifecycle:
    """Tests for browser lifecycle management."""

    @patch('src.tavily_register.core.intelligent_automation.sync_playwright')
    @patch('src.tavily_register.core.intelligent_automation.BROWSER_TYPE', 'chromium')
    def test_start_browser_if_own_browser(self, mock_sync_playwright, automation_without_page):
        """Test browser starts when it owns the browser instance."""
        mock_playwright_instance = Mock()
        mock_browser = Mock()
        mock_page = Mock()
        mock_sync_playwright.return_value.start.return_value = mock_playwright_instance
        mock_playwright_instance.chromium.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page

        automation_without_page.start_browser(headless=True)

        mock_sync_playwright.return_value.start.assert_called_once()
        mock_playwright_instance.chromium.launch.assert_called_once_with(headless=True)
        assert automation_without_page.page is not None

    def test_start_browser_if_not_own_browser(self, automation_with_page):
        """Test browser does not start when a page is provided."""
        with patch('src.tavily_register.core.intelligent_automation.sync_playwright') as mock_sync_playwright:
            automation_with_page.start_browser()
            mock_sync_playwright.return_value.start.assert_not_called()

    def test_close_browser_if_own_browser(self, automation_without_page):
        """Test browser closes when it owns the instance."""
        mock_playwright = Mock()
        mock_browser = Mock()
        mock_page = Mock()

        automation_without_page.playwright = mock_playwright
        automation_without_page.browser = mock_browser
        automation_without_page.page = mock_page

        automation_without_page.close_browser()

        mock_page.close.assert_called_once()
        mock_browser.close.assert_called_once()
        mock_playwright.stop.assert_called_once()
        assert automation_without_page.page is None
        assert automation_without_page.browser is None
        assert automation_without_page.playwright is None

    def test_close_browser_if_not_own_browser(self, automation_with_page):
        """Test browser does not close when a page is provided."""
        mock_page = automation_with_page.page
        automation_with_page.close_browser()
        mock_page.close.assert_not_called()

    @patch('src.tavily_register.core.intelligent_automation.sync_playwright')
    @patch('src.tavily_register.core.intelligent_automation.BROWSER_TYPE', 'firefox')
    def test_start_browser_firefox(self, mock_sync_playwright, automation_without_page):
        """Test that firefox is launched when BROWSER_TYPE is set to firefox."""
        mock_playwright_instance = Mock()
        mock_browser = Mock()
        mock_page = Mock()
        mock_sync_playwright.return_value.start.return_value = mock_playwright_instance
        mock_playwright_instance.firefox.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page

        automation_without_page.start_browser(headless=True)

        mock_playwright_instance.firefox.launch.assert_called_once_with(headless=True)
        mock_playwright_instance.chromium.launch.assert_not_called()


class TestSmartElementWaiting:
    """Tests for the smart element waiting functionality."""

    @pytest.fixture
    def automation(self, mocker):
        """Provides an IntelligentTavilyAutomation instance with a mocked page."""
        automation = IntelligentTavilyAutomation()
        automation.page = mocker.MagicMock(spec=Page)
        return automation

    def test_smart_wait_for_element_primary_success(self, automation, mocker):
        """Test finding an element with a primary selector."""
        mock_element = Mock()
        element_config = {'primary': ['#primary'], 'fallback': ['#fallback']}
        automation.page.wait_for_selector.return_value = mock_element

        element, selector = automation.smart_wait_for_element(element_config)

        assert element is mock_element
        assert selector == '#primary'
        automation.page.wait_for_selector.assert_called_once_with('#primary', timeout=30000)

    def test_smart_wait_for_element_fallback_success(self, automation, mocker):
        """Test finding an element with a fallback selector after primary fails."""
        mock_element = Mock()
        element_config = {'primary': ['#primary'], 'fallback': ['#fallback']}
        automation.page.wait_for_selector.side_effect = [Exception("Primary failed"), mock_element]

        element, selector = automation.smart_wait_for_element(element_config, timeout=10000)

        assert element is mock_element
        assert selector == '#fallback'
        assert automation.page.wait_for_selector.call_count == 2
        
    def test_smart_wait_for_element_not_found(self, automation, mocker):
        """Test when no element is found with any selector."""
        element_config = {'primary': ['#primary'], 'fallback': ['#fallback']}
        automation.page.wait_for_selector.side_effect = Exception("Not found")

        element, selector = automation.smart_wait_for_element(element_config)

        assert element is None
        assert selector is None

    def test_smart_wait_for_element_no_page(self, automation_without_page):
        """Test that it handles the case where the page is None."""
        element, selector = automation_without_page.smart_wait_for_element({})
        assert element is None
        assert selector is None


class TestSmartClick:
    """Tests for the smart_click functionality."""

    @pytest.fixture
    def automation(self, mocker):
        """Provides an IntelligentTavilyAutomation instance with a mocked page."""
        automation = IntelligentTavilyAutomation()
        automation.page = mocker.MagicMock(spec=Page)
        # Mock selectors to avoid key errors
        automation.selectors = {
            'test_button': {
                'primary': ['#test_button']
            }
        }
        return automation

    def test_smart_click_success(self, automation):
        """Test a successful click on the first attempt."""
        mock_element = Mock()
        automation.smart_wait_for_element = Mock(return_value=(mock_element, '#test_button'))

        result = automation.smart_click('test_button')

        assert result is True
        mock_element.click.assert_called_once()
        automation.page.wait_for_load_state.assert_called_once_with('networkidle', timeout=10000)

    def test_smart_click_with_retry(self, automation, mocker):
        """Test a successful click after one failed attempt."""
        mock_element = Mock()
        # First call fails, second call succeeds
        automation.smart_wait_for_element = Mock(side_effect=[
            (None, None),
            (mock_element, '#test_button')
        ])
        mocker.patch.object(automation.page, 'reload')

        result = automation.smart_click('test_button', retries=2)

        assert result is True
        assert automation.smart_wait_for_element.call_count == 2
        automation.page.reload.assert_called_once()
        mock_element.click.assert_called_once()

    def test_smart_click_failure(self, automation):
        """Test a click that fails after all retries."""
        automation.smart_wait_for_element = Mock(return_value=(None, None))

        result = automation.smart_click('test_button', retries=2)

        assert result is False
        assert automation.smart_wait_for_element.call_count == 2
        automation.page.reload.assert_called_once()

    def test_smart_click_no_config(self, automation):
        """Test smart_click with a non-existent element configuration."""
        result = automation.smart_click('non_existent_button')
        assert result is False


class TestSmartFill:
    """Tests for the smart_fill functionality."""

    @pytest.fixture
    def automation(self, mocker):
        """Provides an IntelligentTavilyAutomation instance with a mocked page."""
        automation = IntelligentTavilyAutomation()
        automation.page = mocker.MagicMock(spec=Page)
        automation.selectors = {
            'test_input': {
                'primary': ['#test_input']
            }
        }
        return automation

    def test_smart_fill_success(self, automation):
        """Test a successful fill on the first attempt."""
        mock_element = Mock()
        mock_element.input_value.return_value = "test text"
        automation.smart_wait_for_element = Mock(return_value=(mock_element, '#test_input'))

        result = automation.smart_fill('test_input', 'test text')

        assert result is True
        mock_element.fill.assert_any_call('')
        mock_element.fill.assert_any_call('test text')
        mock_element.input_value.assert_called_once()

    def test_smart_fill_with_retry(self, automation, mocker):
        """Test a successful fill after one failed attempt to find the element."""
        mock_element = Mock()
        mock_element.input_value.return_value = "test text"
        automation.smart_wait_for_element = Mock(side_effect=[
            (None, None),
            (mock_element, '#test_input')
        ])
        mocker.patch.object(automation.page, 'reload')

        result = automation.smart_fill('test_input', 'test text', retries=2)

        assert result is True
        assert automation.smart_wait_for_element.call_count == 2
        automation.page.reload.assert_called_once()
        mock_element.fill.assert_called_with('test text')

    def test_smart_fill_failure(self, automation):
        """Test a fill that fails after all retries."""
        automation.smart_wait_for_element = Mock(return_value=(None, None))

        result = automation.smart_fill('test_input', 'test text', retries=2)

        assert result is False
        assert automation.smart_wait_for_element.call_count == 2
        automation.page.reload.assert_called_once()

    def test_smart_fill_validation_fails(self, automation):
        """Test a fill that fails validation and then succeeds."""
        mock_element = Mock()
        # Fails validation first, then succeeds
        mock_element.input_value.side_effect = ["wrong text", "test text"]
        automation.smart_wait_for_element = Mock(return_value=(mock_element, '#test_input'))

        result = automation.smart_fill('test_input', 'test text', retries=2)

        assert result is True
        assert mock_element.fill.call_count == 4 # (clear, fill) * 2
        assert mock_element.input_value.call_count == 2

    def test_smart_fill_no_config(self, automation):
        """Test smart_fill with a non-existent element configuration."""
        result = automation.smart_fill('non_existent_input', 'test text')
        assert result is False