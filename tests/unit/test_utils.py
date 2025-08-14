"""
Unit tests for utility functions.

Tests the utility helper functions including email generation,
file operations, and logging utilities.
"""
import os
import json
import tempfile
import pytest
from unittest.mock import patch, mock_open
from datetime import datetime

from src.tavily_register.utils.helpers import (
    generate_random_suffix,
    generate_email,
    generate_password,
    save_api_key,
    save_cookies,
    load_cookies,
    wait_with_message,
    log_action,
)


class TestEmailGeneration:
    """Test email generation functions."""

    def test_generate_random_suffix_default_length(self):
        """Test random suffix generation with default length."""
        suffix = generate_random_suffix()
        assert len(suffix) == 8
        assert suffix.isalnum()
        assert suffix.islower()

    def test_generate_random_suffix_custom_length(self):
        """Test random suffix generation with custom length."""
        for length in [4, 12, 16]:
            suffix = generate_random_suffix(length)
            assert len(suffix) == length
            assert suffix.isalnum()
            assert suffix.islower()

    def test_generate_random_suffix_uniqueness(self):
        """Test that random suffixes are unique."""
        suffixes = [generate_random_suffix() for _ in range(100)]
        assert len(set(suffixes)) == 100  # All should be unique

    def test_generate_email_with_default_prefix(self):
        """Test email generation with default prefix."""
        email = generate_email()
        assert "@2925.com" in email
        assert "-" in email  # Should have prefix-suffix format

    def test_generate_email_with_custom_prefix(self):
        """Test email generation with custom prefix."""
        custom_prefix = "test_user"
        email = generate_email(custom_prefix)
        assert email.startswith(custom_prefix)
        assert "@2925.com" in email
        assert "-" in email

    def test_generate_email_format(self):
        """Test email format is correct."""
        email = generate_email("test")
        parts = email.split("@")
        assert len(parts) == 2
        assert parts[1] == "2925.com"
        
        local_part = parts[0]
        assert "-" in local_part
        prefix, suffix = local_part.split("-", 1)
        assert prefix == "test"
        assert len(suffix) == 8

    def test_generate_password(self):
        """Test password generation."""
        password = generate_password()
        assert isinstance(password, str)
        assert len(password) > 0


class TestFileOperations:
    """Test file operation functions."""

    def test_save_api_key_new_file(self):
        """Test saving API key to new file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as tmp:
            tmp_path = tmp.name

        try:
            with patch('src.tavily_register.utils.helpers.API_KEYS_FILE', tmp_path):
                save_api_key("test@example.com", "test-api-key", "password123")
            
            with open(tmp_path, 'r') as f:
                content = f.read()
            
            assert "test@example.com" in content
            assert "test-api-key" in content
            assert "password123" in content
            assert content.endswith(";\n")
        finally:
            os.unlink(tmp_path)

    def test_save_api_key_append_to_existing(self):
        """Test appending API key to existing file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as tmp:
            tmp.write("existing@example.com,pass,key,2025-01-01 00:00:00;\n")
            tmp_path = tmp.name

        try:
            with patch('src.tavily_register.utils.helpers.API_KEYS_FILE', tmp_path):
                save_api_key("new@example.com", "new-key", "newpass")
            
            with open(tmp_path, 'r') as f:
                lines = f.readlines()
            
            assert len(lines) == 2
            assert "existing@example.com" in lines[0]
            assert "new@example.com" in lines[1]
        finally:
            os.unlink(tmp_path)

    def test_save_api_key_without_password(self):
        """Test saving API key without password."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as tmp:
            tmp_path = tmp.name

        try:
            with patch('src.tavily_register.utils.helpers.API_KEYS_FILE', tmp_path):
                save_api_key("test@example.com", "test-key")
            
            with open(tmp_path, 'r') as f:
                content = f.read()
            
            assert "test@example.com" in content
            assert "test-key" in content
            assert "N/A" in content  # Default password value
        finally:
            os.unlink(tmp_path)

    def test_save_cookies(self):
        """Test saving cookies to file."""
        test_cookies = [
            {"name": "session", "value": "abc123", "domain": "example.com"},
            {"name": "auth", "value": "xyz789", "domain": "example.com"}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name

        try:
            save_cookies(test_cookies, tmp_path)
            
            with open(tmp_path, 'r') as f:
                loaded_cookies = json.load(f)
            
            assert loaded_cookies == test_cookies
        finally:
            os.unlink(tmp_path)

    def test_load_cookies_existing_file(self):
        """Test loading cookies from existing file."""
        test_cookies = [{"name": "test", "value": "value"}]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            json.dump(test_cookies, tmp)
            tmp_path = tmp.name

        try:
            loaded_cookies = load_cookies(tmp_path)
            assert loaded_cookies == test_cookies
        finally:
            os.unlink(tmp_path)

    def test_load_cookies_nonexistent_file(self):
        """Test loading cookies from nonexistent file."""
        result = load_cookies("nonexistent_file.json")
        assert result is None


class TestUtilityFunctions:
    """Test utility functions."""

    @patch('time.sleep')
    def test_wait_with_message(self, mock_sleep):
        """Test wait function with message."""
        wait_with_message(5, "Testing")
        mock_sleep.assert_called_once_with(5)

    @patch('time.sleep')
    def test_wait_with_message_default(self, mock_sleep):
        """Test wait function with default message."""
        wait_with_message(3)
        mock_sleep.assert_called_once_with(3)

    @patch('builtins.print')
    def test_log_action_simple(self, mock_print):
        """Test logging action without details."""
        log_action("Test action")
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert "Test action" in call_args
        assert datetime.now().strftime("%Y-%m-%d") in call_args

    @patch('builtins.print')
    def test_log_action_with_details(self, mock_print):
        """Test logging action with details."""
        log_action("Test action", "Additional details")
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert "Test action" in call_args
        assert "Additional details" in call_args


class TestIntegration:
    """Test integration scenarios."""

    def test_email_generation_consistency(self):
        """Test that email generation is consistent with same prefix."""
        prefix = "consistent_test"
        emails = [generate_email(prefix) for _ in range(10)]

        # All should start with same prefix
        for email in emails:
            assert email.startswith(prefix)
            assert "@2925.com" in email

        # All should be unique (due to random suffix)
        assert len(set(emails)) == 10

    def test_file_operations_workflow(self):
        """Test complete file operations workflow."""
        # Test data
        test_cookies = [{"name": "test", "value": "123"}]

        with tempfile.TemporaryDirectory() as tmp_dir:
            cookie_file = os.path.join(tmp_dir, "cookies.json")
            api_file = os.path.join(tmp_dir, "api_keys.md")

            # Save cookies
            save_cookies(test_cookies, cookie_file)
            assert os.path.exists(cookie_file)

            # Load cookies
            loaded = load_cookies(cookie_file)
            assert loaded == test_cookies

            # Save API key
            with patch('src.tavily_register.utils.helpers.API_KEYS_FILE', api_file):
                save_api_key("test@example.com", "api-key-123", "password")

            assert os.path.exists(api_file)

            # Verify API key file content
            with open(api_file, 'r') as f:
                content = f.read()
            assert "test@example.com,password,api-key-123" in content


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_generate_random_suffix_zero_length(self):
        """Test random suffix generation with zero length."""
        suffix = generate_random_suffix(0)
        assert suffix == ""

    def test_generate_random_suffix_very_long(self):
        """Test random suffix generation with very long length."""
        suffix = generate_random_suffix(1000)
        assert len(suffix) == 1000
        assert suffix.isalnum()
        assert suffix.islower()

    def test_generate_email_with_empty_prefix(self):
        """Test email generation with empty prefix."""
        email = generate_email("")
        assert "@2925.com" in email
        assert email.startswith("-")  # Should start with dash due to empty prefix

    def test_generate_email_with_special_characters(self):
        """Test email generation with special characters in prefix."""
        special_prefix = "test-user_123.special"
        email = generate_email(special_prefix)
        assert email.startswith(special_prefix)
        assert "@2925.com" in email

    def test_save_api_key_with_unicode_characters(self):
        """Test saving API key with unicode characters."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as tmp:
            tmp_path = tmp.name

        try:
            with patch('src.tavily_register.utils.helpers.API_KEYS_FILE', tmp_path):
                save_api_key("测试@2925.com", "api-key-unicode", "密码123")

            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()

            assert "测试@2925.com" in content
            assert "密码123" in content
        finally:
            os.unlink(tmp_path)

    def test_save_api_key_with_very_long_values(self):
        """Test saving API key with very long values."""
        long_email = "a" * 100 + "@2925.com"
        long_api_key = "tvly-dev-" + "a" * 1000
        long_password = "b" * 500

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as tmp:
            tmp_path = tmp.name

        try:
            with patch('src.tavily_register.utils.helpers.API_KEYS_FILE', tmp_path):
                save_api_key(long_email, long_api_key, long_password)

            with open(tmp_path, 'r') as f:
                content = f.read()

            assert long_email in content
            assert long_api_key in content
            assert long_password in content
        finally:
            os.unlink(tmp_path)

    def test_load_cookies_with_malformed_json(self):
        """Test loading cookies with malformed JSON."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp.write("{ invalid json content")
            tmp_path = tmp.name

        try:
            result = load_cookies(tmp_path)
            assert result is None
        finally:
            os.unlink(tmp_path)

    def test_save_cookies_with_empty_list(self):
        """Test saving empty cookie list."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name

        try:
            save_cookies([], tmp_path)

            with open(tmp_path, 'r') as f:
                loaded_cookies = json.load(f)

            assert loaded_cookies == []
        finally:
            os.unlink(tmp_path)

    def test_save_cookies_with_complex_data(self):
        """Test saving cookies with complex nested data."""
        complex_cookies = [
            {
                "name": "complex_cookie",
                "value": {"nested": {"data": [1, 2, 3]}, "array": ["a", "b"]},
                "domain": "2925.com",
                "metadata": {"created": "2025-01-01", "expires": None}
            }
        ]

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name

        try:
            save_cookies(complex_cookies, tmp_path)

            loaded_cookies = load_cookies(tmp_path)
            assert loaded_cookies == complex_cookies
        finally:
            os.unlink(tmp_path)


class TestErrorHandling:
    """Test error handling scenarios."""

    def test_save_api_key_permission_denied(self):
        """Test saving API key when file permissions are denied."""
        # Try to write to a directory that doesn't exist
        invalid_path = "/nonexistent/directory/api_keys.md"

        with patch('src.tavily_register.utils.helpers.API_KEYS_FILE', invalid_path):
            # Should handle permission error gracefully
            try:
                save_api_key("test@example.com", "api-key", "password")
            except (PermissionError, FileNotFoundError):
                pass  # Expected behavior

    def test_save_cookies_permission_denied(self):
        """Test saving cookies when file permissions are denied."""
        invalid_path = "/nonexistent/directory/cookies.json"

        with pytest.raises((PermissionError, FileNotFoundError)):
            save_cookies([{"name": "test"}], invalid_path)

    def test_load_cookies_permission_denied(self):
        """Test loading cookies when file permissions are denied."""
        invalid_path = "/nonexistent/directory/cookies.json"

        result = load_cookies(invalid_path)
        assert result is None

    @patch('builtins.open')
    def test_save_api_key_disk_full(self, mock_open):
        """Test saving API key when disk is full."""
        mock_open.side_effect = OSError("No space left on device")

        with patch('src.tavily_register.utils.helpers.API_KEYS_FILE', "test.md"):
            # Should handle disk full error gracefully
            try:
                save_api_key("test@example.com", "api-key", "password")
            except OSError:
                pass  # Expected behavior

    @patch('time.sleep')
    def test_wait_with_message_negative_time(self, mock_sleep):
        """Test wait function with negative time."""
        wait_with_message(-5, "Testing negative wait")
        mock_sleep.assert_called_once_with(-5)

    @patch('time.sleep')
    def test_wait_with_message_zero_time(self, mock_sleep):
        """Test wait function with zero time."""
        wait_with_message(0, "Testing zero wait")
        mock_sleep.assert_called_once_with(0)

    @patch('builtins.print')
    def test_log_action_with_none_message(self, mock_print):
        """Test logging with None message."""
        log_action(None)
        mock_print.assert_called_once()

    @patch('builtins.print')
    def test_log_action_with_empty_message(self, mock_print):
        """Test logging with empty message."""
        log_action("")
        mock_print.assert_called_once()

    @patch('builtins.print')
    def test_log_action_with_very_long_message(self, mock_print):
        """Test logging with very long message."""
        long_message = "a" * 10000
        log_action(long_message)
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert long_message in call_args


class TestPerformance:
    """Test performance-related scenarios."""

    def test_generate_many_emails_performance(self):
        """Test generating many emails for performance."""
        import time

        start_time = time.time()
        emails = [generate_email("perf_test") for _ in range(1000)]
        end_time = time.time()

        # Should complete within reasonable time (less than 1 second)
        assert end_time - start_time < 1.0

        # All emails should be unique
        assert len(set(emails)) == 1000

    def test_large_file_operations(self):
        """Test file operations with large data."""
        # Create large cookie data
        large_cookies = [
            {"name": f"cookie_{i}", "value": "x" * 1000, "domain": "2925.com"}
            for i in range(100)
        ]

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            tmp_path = tmp.name

        try:
            import time
            start_time = time.time()

            save_cookies(large_cookies, tmp_path)
            loaded_cookies = load_cookies(tmp_path)

            end_time = time.time()

            # Should complete within reasonable time
            assert end_time - start_time < 5.0
            assert loaded_cookies == large_cookies
        finally:
            os.unlink(tmp_path)

    def test_concurrent_file_access(self):
        """Test concurrent file access scenarios."""
        import threading
        import time

        results = []

        def save_api_key_worker(worker_id):
            try:
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as tmp:
                    tmp_path = tmp.name

                with patch('src.tavily_register.utils.helpers.API_KEYS_FILE', tmp_path):
                    save_api_key(f"worker{worker_id}@2925.com", f"api-key-{worker_id}", "password")

                results.append(worker_id)
                os.unlink(tmp_path)
            except Exception as e:
                results.append(f"error-{worker_id}")

        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=save_api_key_worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # All workers should complete successfully
        assert len(results) == 5
        assert all(isinstance(r, int) for r in results)
