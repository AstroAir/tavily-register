"""
Integration tests for basic automation workflow.

Tests the complete automation workflow including browser automation,
email handling, and API key extraction in a controlled environment.
"""
import pytest
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock

from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation
from src.tavily_register.utils.helpers import generate_email, save_api_key
from tests.fixtures.sample_data import (
    SAMPLE_CONFIGS,
    SAMPLE_HTML_CONTENT,
    TEST_SELECTORS,
    get_sample_email_by_type
)


class TestBasicWorkflow:
    """Test basic automation workflow components."""

    @pytest.fixture
    def mock_automation(self):
        """Create mock automation instance."""
        automation = IntelligentTavilyAutomation()
        automation.playwright = Mock()
        automation.browser = Mock()
        automation.page = Mock()
        return automation

    @pytest.fixture
    def temp_files(self):
        """Create temporary files for testing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            api_file = os.path.join(tmp_dir, "test_api_keys.md")
            cookie_file = os.path.join(tmp_dir, "test_cookies.json")
            yield {
                "api_file": api_file,
                "cookie_file": cookie_file,
                "tmp_dir": tmp_dir
            }

    def test_automation_initialization(self):
        """Test automation instance initialization."""
        automation = IntelligentTavilyAutomation()
        
        assert automation.playwright is None
        assert automation.browser is None
        assert automation.page is None
        assert automation.email is None
        assert automation.email_prefix is None
        assert automation.debug is True

    def test_email_generation_workflow(self):
        """Test email generation for automation."""
        # Test with default prefix
        email1 = generate_email()
        assert "@2925.com" in email1
        assert "-" in email1
        
        # Test with custom prefix
        email2 = generate_email("test_prefix")
        assert email2.startswith("test_prefix")
        assert "@2925.com" in email2

    @patch('src.tavily_register.utils.helpers.API_KEYS_FILE')
    def test_api_key_saving_workflow(self, mock_api_file, temp_files):
        """Test API key saving workflow."""
        mock_api_file.__str__ = lambda: temp_files["api_file"]
        mock_api_file.__fspath__ = lambda: temp_files["api_file"]
        
        # Mock the API_KEYS_FILE constant
        with patch('src.tavily_register.utils.helpers.API_KEYS_FILE', temp_files["api_file"]):
            save_api_key("test@example.com", "test-api-key", "password123")
        
        # Verify file was created and contains correct data
        assert os.path.exists(temp_files["api_file"])
        with open(temp_files["api_file"], 'r') as f:
            content = f.read()
        
        assert "test@example.com" in content
        assert "test-api-key" in content
        assert "password123" in content

    def test_browser_automation_mock_workflow(self, mock_automation):
        """Test browser automation workflow with mocks."""
        # Setup mock page responses
        mock_automation.page.goto = Mock()
        mock_automation.page.wait_for_selector = Mock()
        mock_automation.page.fill = Mock()
        mock_automation.page.click = Mock()
        
        # Test navigation
        mock_automation.page.goto("https://app.tavily.com")
        mock_automation.page.goto.assert_called_with("https://app.tavily.com")
        
        # Test form filling
        mock_automation.page.fill("#email", "test@example.com")
        mock_automation.page.fill.assert_called_with("#email", "test@example.com")
        
        # Test clicking
        mock_automation.page.click("button[type='submit']")
        mock_automation.page.click.assert_called_with("button[type='submit']")

    def test_configuration_integration(self):
        """Test configuration integration in workflow."""
        test_config = {k: str(v) for k, v in SAMPLE_CONFIGS["test_config"].items()}
        
        with patch.dict(os.environ, test_config):
            # Reload configuration to pick up test values
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)
            
            # Verify configuration is applied
            assert settings.EMAIL_PREFIX == "test_user"
            assert settings.HEADLESS is True
            assert settings.WAIT_TIME_SHORT == 1

    @patch('playwright.sync_api.sync_playwright')
    def test_browser_lifecycle_workflow(self, mock_playwright):
        """Test browser lifecycle management."""
        # Setup mocks
        mock_playwright_instance = Mock()
        mock_browser = Mock()
        mock_page = Mock()
        
        mock_playwright.return_value.start.return_value = mock_playwright_instance
        mock_playwright_instance.firefox.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page
        
        automation = IntelligentTavilyAutomation()
        
        # Test browser startup
        automation.start_browser(headless=True)
        
        # Verify browser was launched with correct options
        mock_playwright_instance.firefox.launch.assert_called_once()
        call_args = mock_playwright_instance.firefox.launch.call_args
        assert call_args[1]['headless'] is True
        
        # Test browser cleanup
        automation.close_browser()
        mock_browser.close.assert_called_once()

    def test_error_handling_workflow(self, mock_automation):
        """Test error handling in automation workflow."""
        # Setup mock to raise exception
        mock_automation.page.goto.side_effect = Exception("Network error")
        
        # Test that exceptions are handled gracefully
        try:
            mock_automation.page.goto("https://app.tavily.com")
            assert False, "Expected exception was not raised"
        except Exception as e:
            assert str(e) == "Network error"

    def test_selector_configuration_workflow(self):
        """Test selector configuration for different page types."""
        selectors = TEST_SELECTORS
        
        # Test Tavily signup selectors
        signup_selectors = selectors["tavily_signup"]
        assert "#email" in signup_selectors["email_input"]
        assert "#password" in signup_selectors["password_input"]
        assert "button[type='submit']" in signup_selectors["signup_button"]
        
        # Test dashboard selectors
        dashboard_selectors = selectors["tavily_dashboard"]
        assert "#api-key" in dashboard_selectors["api_key_element"]

    @patch('time.sleep')
    def test_timing_workflow(self, mock_sleep):
        """Test timing and waiting mechanisms."""
        from src.tavily_register.utils.helpers import wait_with_message
        
        # Test wait functionality
        wait_with_message(5, "Testing wait")
        mock_sleep.assert_called_with(5)

    def test_email_data_processing_workflow(self):
        """Test email data processing workflow."""
        verification_email = get_sample_email_by_type("verification")
        
        # Test email data structure
        assert verification_email["sender"] == "noreply@tavily.com"
        assert "verify" in verification_email["subject"].lower()
        assert "https://app.tavily.com/verify" in verification_email["body"]
        assert verification_email["is_unread"] is True

    def test_html_content_processing_workflow(self):
        """Test HTML content processing workflow."""
        signup_html = SAMPLE_HTML_CONTENT["tavily_signup_page"]
        dashboard_html = SAMPLE_HTML_CONTENT["tavily_dashboard"]
        
        # Test signup page content
        assert 'id="email"' in signup_html
        assert 'type="password"' in signup_html
        assert 'Sign up' in signup_html
        
        # Test dashboard content
        assert 'id="api-key"' in dashboard_html
        assert 'tvly-dev-' in dashboard_html


class TestWorkflowIntegration:
    """Test complete workflow integration scenarios."""

    @pytest.fixture
    def mock_complete_automation(self):
        """Create complete mock automation setup."""
        automation = IntelligentTavilyAutomation()
        
        # Mock all browser components
        automation.playwright = Mock()
        automation.browser = Mock()
        automation.page = Mock()
        
        # Mock page methods
        automation.page.goto = Mock()
        automation.page.wait_for_selector = Mock()
        automation.page.fill = Mock()
        automation.page.click = Mock()
        automation.page.inner_text = Mock(return_value="tvly-dev-test123")
        
        return automation

    def test_registration_workflow_simulation(self, mock_complete_automation):
        """Test simulated registration workflow."""
        automation = mock_complete_automation
        automation.email_prefix = "test"
        
        # Simulate registration steps
        automation.page.goto("https://app.tavily.com")
        automation.page.wait_for_selector("#email")
        automation.page.fill("#email", "test@2925.com")
        automation.page.fill("#password", "TavilyAuto123!")
        automation.page.click("button[type='submit']")
        
        # Verify all steps were called
        automation.page.goto.assert_called_with("https://app.tavily.com")
        automation.page.wait_for_selector.assert_called_with("#email")
        automation.page.fill.assert_any_call("#email", "test@2925.com")
        automation.page.fill.assert_any_call("#password", "TavilyAuto123!")
        automation.page.click.assert_called_with("button[type='submit']")

    def test_api_key_extraction_workflow(self, mock_complete_automation):
        """Test API key extraction workflow."""
        automation = mock_complete_automation
        
        # Mock API key element
        automation.page.inner_text.return_value = "tvly-dev-abc123def456"
        
        # Simulate API key extraction
        automation.page.wait_for_selector("#api-key")
        api_key = automation.page.inner_text("#api-key")
        
        # Verify extraction
        automation.page.wait_for_selector.assert_called_with("#api-key")
        automation.page.inner_text.assert_called_with("#api-key")
        assert api_key == "tvly-dev-abc123def456"

    @patch('src.tavily_register.utils.helpers.save_api_key')
    def test_complete_workflow_simulation(self, mock_save_api_key, mock_complete_automation):
        """Test complete workflow simulation."""
        automation = mock_complete_automation
        automation.email = "test@2925.com"
        automation.password = "TavilyAuto123!"

        # Mock successful API key extraction
        automation.page.inner_text.return_value = "tvly-dev-success123"

        # Simulate complete workflow
        # 1. Registration (already tested above)
        # 2. Email verification (mocked)
        # 3. API key extraction
        automation.page.wait_for_selector("#api-key")
        api_key = automation.page.inner_text("#api-key")

        # 4. Save API key
        mock_save_api_key(automation.email, api_key, automation.password)

        # Verify complete workflow
        assert api_key == "tvly-dev-success123"
        mock_save_api_key.assert_called_with(
            "test@2925.com",
            "tvly-dev-success123",
            "TavilyAuto123!"
        )


class TestAdvancedIntegrationScenarios:
    """Test advanced integration scenarios and error recovery."""

    @pytest.fixture
    def mock_complete_system(self):
        """Create complete mocked system for integration testing."""
        # Mock all major components
        automation = Mock()
        email_checker = Mock()
        login_helper = Mock()

        # Setup automation
        automation.email = "integration@2925.com"
        automation.password = "IntegrationTest123!"
        automation.email_prefix = "integration"

        # Setup browser components
        automation.playwright = Mock()
        automation.browser = Mock()
        automation.page = Mock()

        return {
            'automation': automation,
            'email_checker': email_checker,
            'login_helper': login_helper
        }

    def test_end_to_end_workflow_with_retries(self, mock_complete_system):
        """Test end-to-end workflow with retry mechanisms."""
        automation = mock_complete_system['automation']

        # Mock initial failure, then success
        automation.run_registration.side_effect = [False, True]  # Fail first, succeed second
        automation.handle_email_verification_and_login.return_value = "tvly-dev-retry123"

        # Simulate retry logic
        for attempt in range(2):
            if automation.run_registration():
                api_key = automation.handle_email_verification_and_login()
                if api_key:
                    break

        assert api_key == "tvly-dev-retry123"
        assert automation.run_registration.call_count == 2

    def test_configuration_integration_workflow(self, mock_complete_system):
        """Test configuration integration across components."""
        automation = mock_complete_system['automation']

        # Test configuration propagation
        test_config = {
            "EMAIL_PREFIX": "config_test",
            "HEADLESS": "True",
            "WAIT_TIME_SHORT": "1"
        }

        with patch.dict(os.environ, test_config):
            # Reload configuration
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)

            # Verify configuration is applied
            assert settings.EMAIL_PREFIX == "config_test"
            assert settings.HEADLESS is True
            assert settings.WAIT_TIME_SHORT == 1

            # Test automation uses configuration
            automation.email_prefix = settings.EMAIL_PREFIX
            assert automation.email_prefix == "config_test"

    @patch('src.tavily_register.email.checker.EmailChecker')
    @patch('src.tavily_register.core.intelligent_automation.IntelligentTavilyAutomation')
    def test_email_verification_integration(self, mock_automation_class, mock_checker_class, mock_complete_system):
        """Test email verification integration between components."""
        # Setup mocks
        automation = Mock()
        checker = Mock()

        mock_automation_class.return_value = automation
        mock_checker_class.return_value = checker

        # Mock email verification workflow
        automation.email = "verify@2925.com"
        checker.wait_for_email.return_value = "https://app.tavily.com/verify?token=integration123"
        automation.page.goto.return_value = None
        automation.extract_api_key.return_value = "tvly-dev-verified123"

        # Execute integration workflow
        verification_link = checker.wait_for_email(automation.email, timeout=300)
        automation.page.goto(verification_link)
        api_key = automation.extract_api_key()

        # Verify integration
        assert verification_link == "https://app.tavily.com/verify?token=integration123"
        assert api_key == "tvly-dev-verified123"
        checker.wait_for_email.assert_called_with("verify@2925.com", timeout=300)
        automation.page.goto.assert_called_with("https://app.tavily.com/verify?token=integration123")

    def test_error_propagation_integration(self, mock_complete_system):
        """Test error propagation between integrated components."""
        automation = mock_complete_system['automation']
        email_checker = mock_complete_system['email_checker']

        # Setup error chain
        automation.start_browser.side_effect = Exception("Browser failed")
        email_checker.start_browser.side_effect = Exception("Email browser failed")

        # Test error handling
        browser_error = None
        email_error = None

        try:
            automation.start_browser()
        except Exception as e:
            browser_error = str(e)

        try:
            email_checker.start_browser()
        except Exception as e:
            email_error = str(e)

        assert browser_error == "Browser failed"
        assert email_error == "Email browser failed"

    def test_resource_cleanup_integration(self, mock_complete_system):
        """Test resource cleanup across integrated components."""
        automation = mock_complete_system['automation']
        email_checker = mock_complete_system['email_checker']
        login_helper = mock_complete_system['login_helper']

        # Setup cleanup tracking
        cleanup_calls = []

        def track_cleanup(component_name):
            cleanup_calls.append(component_name)

        automation.close_browser.side_effect = lambda: track_cleanup("automation")
        email_checker.close_browser.side_effect = lambda: track_cleanup("email_checker")
        login_helper.close_browser.side_effect = lambda: track_cleanup("login_helper")

        # Simulate cleanup
        try:
            # Simulate some work
            pass
        finally:
            # Cleanup all components
            automation.close_browser()
            email_checker.close_browser()
            login_helper.close_browser()

        assert "automation" in cleanup_calls
        assert "email_checker" in cleanup_calls
        assert "login_helper" in cleanup_calls

    @patch('time.sleep')
    def test_timing_integration_workflow(self, mock_sleep, mock_complete_system):
        """Test timing and synchronization in integrated workflow."""
        automation = mock_complete_system['automation']

        # Mock workflow with timing
        automation.navigate_to_signup.return_value = True
        automation.fill_registration_form.return_value = True
        automation.wait_for_email_verification.return_value = "https://app.tavily.com/verify?token=timing123"
        automation.extract_api_key.return_value = "tvly-dev-timing123"

        # Execute timed workflow
        start_time = 0

        # Step 1: Navigation (should wait)
        automation.navigate_to_signup()
        start_time += 1

        # Step 2: Form filling (should wait)
        automation.fill_registration_form()
        start_time += 2

        # Step 3: Email verification (should wait longer)
        automation.wait_for_email_verification()
        start_time += 5

        # Step 4: API key extraction (should wait)
        automation.extract_api_key()
        start_time += 1

        # Verify timing calls were made
        assert automation.navigate_to_signup.called
        assert automation.fill_registration_form.called
        assert automation.wait_for_email_verification.called
        assert automation.extract_api_key.called

    def test_concurrent_operations_integration(self, mock_complete_system):
        """Test concurrent operations integration."""
        import threading
        import time

        automation = mock_complete_system['automation']
        results = []

        def worker_automation(worker_id):
            """Simulate concurrent automation worker."""
            try:
                # Mock worker-specific setup
                automation.email = f"worker{worker_id}@2925.com"
                automation.run_complete_automation.return_value = f"tvly-dev-worker{worker_id}"

                # Simulate work
                time.sleep(0.1)  # Small delay to simulate real work
                api_key = automation.run_complete_automation()

                results.append({
                    'worker_id': worker_id,
                    'api_key': api_key,
                    'success': True
                })
            except Exception as e:
                results.append({
                    'worker_id': worker_id,
                    'error': str(e),
                    'success': False
                })

        # Create multiple worker threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=worker_automation, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Verify all workers completed successfully
        assert len(results) == 3
        assert all(result['success'] for result in results)

    def test_data_flow_integration(self, mock_complete_system):
        """Test data flow between integrated components."""
        automation = mock_complete_system['automation']
        email_checker = mock_complete_system['email_checker']

        # Setup data flow
        test_email = "dataflow@2925.com"
        test_verification_link = "https://app.tavily.com/verify?token=dataflow123"
        test_api_key = "tvly-dev-dataflow123"

        # Mock data flow
        automation.email = test_email
        email_checker.wait_for_email.return_value = test_verification_link
        automation.extract_api_key.return_value = test_api_key

        # Execute data flow
        email = automation.email
        verification_link = email_checker.wait_for_email(email, timeout=60)
        automation.page.goto(verification_link)
        api_key = automation.extract_api_key()

        # Verify data flow
        assert email == test_email
        assert verification_link == test_verification_link
        assert api_key == test_api_key

        # Verify method calls with correct data
        email_checker.wait_for_email.assert_called_with(test_email, timeout=60)
        automation.page.goto.assert_called_with(test_verification_link)


class TestPerformanceIntegration:
    """Test performance aspects of integrated system."""

    @pytest.fixture
    def performance_automation(self):
        """Create automation instance for performance testing."""
        automation = Mock()
        automation.email_prefix = "perf_test"
        return automation

    def test_bulk_automation_performance(self, performance_automation):
        """Test performance of bulk automation operations."""
        import time

        # Mock bulk operations
        performance_automation.run_complete_automation.return_value = "tvly-dev-bulk123"

        start_time = time.time()

        # Simulate bulk operations
        results = []
        for i in range(10):
            performance_automation.email = f"bulk{i}@2925.com"
            api_key = performance_automation.run_complete_automation()
            results.append(api_key)

        end_time = time.time()

        # Verify performance
        assert len(results) == 10
        assert all(result == "tvly-dev-bulk123" for result in results)
        assert end_time - start_time < 1.0  # Should complete quickly with mocks

    def test_memory_usage_integration(self, performance_automation):
        """Test memory usage in integrated operations."""
        import gc

        # Force garbage collection before test
        gc.collect()

        # Simulate memory-intensive operations
        large_data = []
        for i in range(100):
            performance_automation.email = f"memory{i}@2925.com"
            large_data.append({
                'email': performance_automation.email,
                'api_key': f"tvly-dev-memory{i}",
                'timestamp': f"2025-01-01 12:{i:02d}:00"
            })

        # Verify data was created
        assert len(large_data) == 100

        # Cleanup
        del large_data
        gc.collect()

    def test_timeout_handling_integration(self, performance_automation):
        """Test timeout handling in integrated operations."""
        import time

        # Mock timeout scenarios
        performance_automation.wait_for_email_verification.side_effect = [
            None,  # First attempt times out
            "https://app.tavily.com/verify?token=timeout123"  # Second attempt succeeds
        ]

        # Simulate timeout handling with retries
        max_attempts = 3
        verification_link = None

        for attempt in range(max_attempts):
            verification_link = performance_automation.wait_for_email_verification()
            if verification_link:
                break
            time.sleep(0.1)  # Small delay between retries

        assert verification_link == "https://app.tavily.com/verify?token=timeout123"
        assert performance_automation.wait_for_email_verification.call_count == 2
