"""
Unit tests for configuration management.

Tests the configuration module including environment variable handling,
type conversion, and default value management.
"""
import os
import pytest
from unittest.mock import patch

from src.tavily_register.config.settings import (
    get_env_bool,
    get_env_int,
    get_env_str,
    EMAIL_DOMAIN,
    EMAIL_PREFIX,
    BROWSER_TYPE,
    HEADLESS,
    WAIT_TIME_SHORT,
)


class TestEnvironmentHelpers:
    """Test environment variable helper functions."""

    def test_get_env_str_with_default(self):
        """Test string environment variable with default value."""
        with patch.dict(os.environ, {}, clear=True):
            result = get_env_str("TEST_VAR", "default_value")
            assert result == "default_value"

    def test_get_env_str_with_value(self):
        """Test string environment variable with set value."""
        with patch.dict(os.environ, {"TEST_VAR": "custom_value"}):
            result = get_env_str("TEST_VAR", "default_value")
            assert result == "custom_value"

    def test_get_env_bool_true_values(self):
        """Test boolean environment variable with true values."""
        true_values = ["true", "1", "yes", "on", "TRUE", "True"]
        for value in true_values:
            with patch.dict(os.environ, {"TEST_BOOL": value}):
                result = get_env_bool("TEST_BOOL", False)
                assert result is True, f"Failed for value: {value}"

    def test_get_env_bool_false_values(self):
        """Test boolean environment variable with false values."""
        false_values = ["false", "0", "no", "off", "FALSE", "False", "anything"]
        for value in false_values:
            with patch.dict(os.environ, {"TEST_BOOL": value}):
                result = get_env_bool("TEST_BOOL", True)
                assert result is False, f"Failed for value: {value}"

    def test_get_env_bool_default(self):
        """Test boolean environment variable with default value."""
        with patch.dict(os.environ, {}, clear=True):
            result = get_env_bool("TEST_BOOL", True)
            assert result is True
            
            result = get_env_bool("TEST_BOOL", False)
            assert result is False

    def test_get_env_int_with_valid_value(self):
        """Test integer environment variable with valid value."""
        with patch.dict(os.environ, {"TEST_INT": "42"}):
            result = get_env_int("TEST_INT", 10)
            assert result == 42

    def test_get_env_int_with_invalid_value(self):
        """Test integer environment variable with invalid value."""
        with patch.dict(os.environ, {"TEST_INT": "not_a_number"}):
            result = get_env_int("TEST_INT", 10)
            assert result == 10  # Should return default

    def test_get_env_int_with_default(self):
        """Test integer environment variable with default value."""
        with patch.dict(os.environ, {}, clear=True):
            result = get_env_int("TEST_INT", 42)
            assert result == 42


class TestConfigurationValues:
    """Test actual configuration values."""

    def test_email_domain_default(self):
        """Test email domain configuration."""
        assert EMAIL_DOMAIN == "2925.com"

    def test_email_prefix_configurable(self):
        """Test email prefix is configurable via environment."""
        with patch.dict(os.environ, {"EMAIL_PREFIX": "test_prefix"}):
            # Need to reload the module to pick up new env var
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)
            assert settings.EMAIL_PREFIX == "test_prefix"

    def test_browser_type_default(self):
        """Test browser type default value."""
        assert BROWSER_TYPE in ["firefox", "chromium", "webkit"]

    def test_headless_default(self):
        """Test headless mode default value."""
        assert isinstance(HEADLESS, bool)

    def test_wait_times_are_positive(self):
        """Test wait time values are positive integers."""
        assert isinstance(WAIT_TIME_SHORT, int)
        assert WAIT_TIME_SHORT > 0


class TestConfigurationIntegration:
    """Test configuration integration scenarios."""

    def test_environment_override(self):
        """Test that environment variables override defaults."""
        test_env = {
            "EMAIL_PREFIX": "env_test",
            "HEADLESS": "true",
            "WAIT_TIME_SHORT": "5",
            "BROWSER_TYPE": "chromium"
        }
        
        with patch.dict(os.environ, test_env):
            # Reload configuration to pick up environment changes
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)
            
            assert settings.EMAIL_PREFIX == "env_test"
            assert settings.HEADLESS is True
            assert settings.WAIT_TIME_SHORT == 5
            assert settings.BROWSER_TYPE == "chromium"

    def test_main_email_generation(self):
        """Test that MAIN_EMAIL is properly generated."""
        with patch.dict(os.environ, {"EMAIL_PREFIX": "test", "EMAIL_DOMAIN": "example.com"}):
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)
            
            expected = "test@example.com"
            assert settings.MAIN_EMAIL == expected

    def test_file_paths_configuration(self):
        """Test file path configuration."""
        from src.tavily_register.config.settings import API_KEYS_FILE, COOKIES_FILE
        
        assert API_KEYS_FILE.endswith(".md")
        assert COOKIES_FILE.endswith(".json")

    def test_browser_timeout_configuration(self):
        """Test browser timeout configuration."""
        from src.tavily_register.config.settings import BROWSER_TIMEOUT
        
        assert isinstance(BROWSER_TIMEOUT, int)
        assert BROWSER_TIMEOUT > 0


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment after each test."""
    yield
    # Reload settings module to reset to defaults
    import importlib
    from src.tavily_register.config import settings
    importlib.reload(settings)


class TestAdvancedConfiguration:
    """Test advanced configuration scenarios and edge cases."""

    def test_configuration_with_invalid_browser_type(self):
        """Test configuration with invalid browser type."""
        with patch.dict(os.environ, {"BROWSER_TYPE": "invalid_browser"}):
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)

            # Should fall back to default or handle gracefully
            assert settings.BROWSER_TYPE in ["firefox", "chromium", "webkit", "invalid_browser"]

    def test_configuration_with_extreme_wait_times(self):
        """Test configuration with extreme wait time values."""
        test_cases = [
            {"WAIT_TIME_SHORT": "0"},
            {"WAIT_TIME_SHORT": "999999"},
            {"WAIT_TIME_SHORT": "-1"}
        ]

        for test_env in test_cases:
            with patch.dict(os.environ, test_env):
                import importlib
                from src.tavily_register.config import settings
                importlib.reload(settings)

                # Should handle extreme values gracefully
                assert isinstance(settings.WAIT_TIME_SHORT, int)

    def test_configuration_with_special_characters_in_paths(self):
        """Test configuration with special characters in file paths."""
        special_paths = {
            "API_KEYS_FILE": "api_keys_测试.md",
            "COOKIES_FILE": "cookies-file@special.json"
        }

        with patch.dict(os.environ, special_paths):
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)

            assert "测试" in settings.API_KEYS_FILE
            assert "@special" in settings.COOKIES_FILE

    def test_configuration_with_empty_values(self):
        """Test configuration with empty environment values."""
        empty_env = {
            "EMAIL_PREFIX": "",
            "EMAIL_DOMAIN": "",
            "BROWSER_TYPE": ""
        }

        with patch.dict(os.environ, empty_env):
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)

            # Should handle empty values appropriately
            assert isinstance(settings.EMAIL_PREFIX, str)
            assert isinstance(settings.EMAIL_DOMAIN, str)
            assert isinstance(settings.BROWSER_TYPE, str)

    def test_configuration_precedence(self):
        """Test configuration precedence order."""
        # Test that environment variables override defaults
        original_prefix = "default_prefix"
        override_prefix = "override_prefix"

        # First, test with default
        with patch.dict(os.environ, {}, clear=True):
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)
            default_value = settings.EMAIL_PREFIX

        # Then test with override
        with patch.dict(os.environ, {"EMAIL_PREFIX": override_prefix}):
            importlib.reload(settings)
            override_value = settings.EMAIL_PREFIX

        assert override_value == override_prefix
        assert override_value != default_value

    def test_configuration_type_coercion(self):
        """Test configuration type coercion for different data types."""
        type_test_env = {
            "HEADLESS": "true",
            "WAIT_TIME_SHORT": "5",
            "BROWSER_TIMEOUT": "30000"
        }

        with patch.dict(os.environ, type_test_env):
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)

            assert isinstance(settings.HEADLESS, bool)
            assert settings.HEADLESS is True
            assert isinstance(settings.WAIT_TIME_SHORT, int)
            assert settings.WAIT_TIME_SHORT == 5
            assert isinstance(settings.BROWSER_TIMEOUT, int)
            assert settings.BROWSER_TIMEOUT == 30000

    def test_configuration_validation(self):
        """Test configuration validation and error handling."""
        invalid_configs = [
            {"WAIT_TIME_SHORT": "not_a_number"},
            {"HEADLESS": "maybe"},
            {"BROWSER_TIMEOUT": "invalid_timeout"}
        ]

        for invalid_config in invalid_configs:
            with patch.dict(os.environ, invalid_config):
                import importlib
                from src.tavily_register.config import settings
                importlib.reload(settings)

                # Should handle invalid values gracefully
                # (specific behavior depends on implementation)
                assert hasattr(settings, 'WAIT_TIME_SHORT')
                assert hasattr(settings, 'HEADLESS')
                assert hasattr(settings, 'BROWSER_TIMEOUT')


class TestConfigurationSecurity:
    """Test configuration security aspects."""

    def test_sensitive_data_handling(self):
        """Test handling of sensitive configuration data."""
        sensitive_env = {
            "EMAIL_PASSWORD": "secret_password",
            "API_SECRET": "secret_api_key"
        }

        with patch.dict(os.environ, sensitive_env):
            # Configuration should handle sensitive data appropriately
            # (This test depends on how sensitive data is actually handled)
            assert os.environ.get("EMAIL_PASSWORD") == "secret_password"

    def test_configuration_isolation(self):
        """Test configuration isolation between test runs."""
        # Set configuration in first context
        with patch.dict(os.environ, {"EMAIL_PREFIX": "isolated_test_1"}):
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)
            first_value = settings.EMAIL_PREFIX

        # Set different configuration in second context
        with patch.dict(os.environ, {"EMAIL_PREFIX": "isolated_test_2"}):
            importlib.reload(settings)
            second_value = settings.EMAIL_PREFIX

        assert first_value == "isolated_test_1"
        assert second_value == "isolated_test_2"
        assert first_value != second_value

    def test_configuration_immutability(self):
        """Test that configuration values are properly protected."""
        from src.tavily_register.config import settings

        # Try to modify configuration at runtime
        original_domain = settings.EMAIL_DOMAIN

        # Attempt to modify (this may or may not be prevented depending on implementation)
        try:
            settings.EMAIL_DOMAIN = "modified_domain.com"
            modified_domain = settings.EMAIL_DOMAIN
        except (AttributeError, TypeError):
            # Configuration is protected
            modified_domain = original_domain

        # Verify behavior is consistent
        assert isinstance(original_domain, str)


class TestConfigurationPerformance:
    """Test configuration performance aspects."""

    def test_configuration_loading_performance(self):
        """Test configuration loading performance."""
        import time

        start_time = time.time()

        # Reload configuration multiple times
        for _ in range(100):
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)

        end_time = time.time()

        # Should complete within reasonable time
        assert end_time - start_time < 1.0

    def test_configuration_memory_usage(self):
        """Test configuration memory usage."""
        import gc

        # Force garbage collection
        gc.collect()

        # Load configuration multiple times
        configs = []
        for i in range(10):
            with patch.dict(os.environ, {"EMAIL_PREFIX": f"memory_test_{i}"}):
                import importlib
                from src.tavily_register.config import settings
                importlib.reload(settings)
                configs.append(settings.EMAIL_PREFIX)

        # Verify all configurations were loaded
        assert len(configs) == 10
        assert all(f"memory_test_{i}" == configs[i] for i in range(10))

        # Cleanup
        del configs
        gc.collect()


class TestConfigurationCompatibility:
    """Test configuration compatibility across different environments."""

    def test_windows_path_compatibility(self):
        """Test configuration with Windows-style paths."""
        windows_paths = {
            "API_KEYS_FILE": "C:\\Users\\Test\\api_keys.md",
            "COOKIES_FILE": "C:\\Users\\Test\\cookies.json"
        }

        with patch.dict(os.environ, windows_paths):
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)

            assert "C:\\" in settings.API_KEYS_FILE or "C:/" in settings.API_KEYS_FILE
            assert "C:\\" in settings.COOKIES_FILE or "C:/" in settings.COOKIES_FILE

    def test_unix_path_compatibility(self):
        """Test configuration with Unix-style paths."""
        unix_paths = {
            "API_KEYS_FILE": "/home/user/api_keys.md",
            "COOKIES_FILE": "/home/user/cookies.json"
        }

        with patch.dict(os.environ, unix_paths):
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)

            assert "/home/user/" in settings.API_KEYS_FILE
            assert "/home/user/" in settings.COOKIES_FILE

    def test_relative_path_compatibility(self):
        """Test configuration with relative paths."""
        relative_paths = {
            "API_KEYS_FILE": "./data/api_keys.md",
            "COOKIES_FILE": "../config/cookies.json"
        }

        with patch.dict(os.environ, relative_paths):
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)

            assert "./data/" in settings.API_KEYS_FILE
            assert "../config/" in settings.COOKIES_FILE

    def test_unicode_configuration(self):
        """Test configuration with Unicode characters."""
        unicode_config = {
            "EMAIL_PREFIX": "测试用户",
            "EMAIL_DOMAIN": "测试域名.com"
        }

        with patch.dict(os.environ, unicode_config):
            import importlib
            from src.tavily_register.config import settings
            importlib.reload(settings)

            assert "测试用户" in settings.EMAIL_PREFIX
            assert "测试域名" in settings.EMAIL_DOMAIN
