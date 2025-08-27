"""
Performance benchmarks for Tavily Register components.

These tests measure the performance of key operations to ensure
they meet acceptable performance standards.
"""
import pytest
import time
from unittest.mock import Mock, patch
from concurrent.futures import ThreadPoolExecutor

from src.tavily_register.utils.helpers import generate_email, save_api_key
from src.tavily_register.config import settings
from src.tavily_register.email.checker import EmailChecker


class TestPerformanceBenchmarks:
    """Performance benchmark tests."""

    def test_email_generation_performance(self, benchmark):
        """Benchmark email generation performance."""
        def generate_multiple_emails():
            emails = []
            for i in range(100):
                email = generate_email(f"user{i}")
                emails.append(email)
            return emails

        result = benchmark(generate_multiple_emails)
        assert len(result) == 100
        assert all("@2925.com" in email for email in result)

    def test_config_loading_performance(self, benchmark):
        """Benchmark configuration loading performance."""
        def load_config_multiple_times():
            configs = []
            for _ in range(50):
                # Test loading configuration values
                config = {
                    'browser_type': settings.BROWSER_TYPE,
                    'headless': settings.HEADLESS,
                    'timeout': settings.BROWSER_TIMEOUT
                }
                configs.append(config)
            return configs

        result = benchmark(load_config_multiple_times)
        assert len(result) == 50

    @patch('src.tavily_register.email.checker.requests.get')
    def test_email_checking_performance(self, mock_get, benchmark):
        """Benchmark email checking performance."""
        # Mock successful email check response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"email": "test@2925.com", "status": "success"}
        mock_get.return_value = mock_response

        checker = EmailChecker()

        def check_multiple_emails():
            results = []
            for i in range(20):
                email = f"test{i}@2925.com"
                result = checker.check_email(email)
                results.append(result)
            return results

        result = benchmark(check_multiple_emails)
        assert len(result) == 20

    def test_concurrent_email_generation_performance(self, benchmark):
        """Benchmark concurrent email generation."""
        def generate_emails_concurrently():
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                for i in range(100):
                    future = executor.submit(generate_email, f"concurrent{i}")
                    futures.append(future)
                
                results = [future.result() for future in futures]
                return results

        result = benchmark(generate_emails_concurrently)
        assert len(result) == 100
        assert all("@2925.com" in email for email in result)

    def test_memory_usage_performance(self, benchmark):
        """Benchmark memory usage during operations."""
        import gc
        
        def memory_intensive_operation():
            # Force garbage collection before test
            gc.collect()
            
            # Create large data structures
            large_data = []
            for i in range(1000):
                email_data = {
                    'email': generate_email(f"memory{i}"),
                    'timestamp': time.time(),
                    'config': get_config(),
                    'metadata': {
                        'iteration': i,
                        'batch': i // 100,
                        'data': f"test_data_{i}" * 10
                    }
                }
                large_data.append(email_data)
            
            # Process the data
            processed = []
            for item in large_data:
                processed_item = {
                    'email': item['email'],
                    'processed_at': time.time(),
                    'size': len(str(item))
                }
                processed.append(processed_item)
            
            # Cleanup
            del large_data
            gc.collect()
            
            return processed

        result = benchmark(memory_intensive_operation)
        assert len(result) == 1000

    @patch('builtins.open', create=True)
    def test_file_operations_performance(self, mock_open, benchmark):
        """Benchmark file operations performance."""
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file

        def file_operations():
            results = []
            for i in range(50):
                email = f"filetest{i}@2925.com"
                api_key = f"tvly-dev-filetest{i}"
                password = f"FileTest{i}!"
                
                # Simulate saving API key (file operation)
                save_api_key(email, api_key, password)
                results.append((email, api_key))
            
            return results

        result = benchmark(file_operations)
        assert len(result) == 50

    def test_string_processing_performance(self, benchmark):
        """Benchmark string processing operations."""
        def string_processing():
            results = []
            base_text = "tavily_register_performance_test"
            
            for i in range(1000):
                # Various string operations
                processed = base_text.upper()
                processed = processed.lower()
                processed = processed.replace("_", "-")
                processed = f"{processed}_{i}"
                processed = processed.split("-")
                processed = "-".join(processed)
                
                results.append(processed)
            
            return results

        result = benchmark(string_processing)
        assert len(result) == 1000

    def test_data_structure_performance(self, benchmark):
        """Benchmark data structure operations."""
        def data_structure_operations():
            # List operations
            data_list = []
            for i in range(500):
                data_list.append(f"item_{i}")
            
            # Dictionary operations
            data_dict = {}
            for i in range(500):
                data_dict[f"key_{i}"] = f"value_{i}"
            
            # Set operations
            data_set = set()
            for i in range(500):
                data_set.add(f"set_item_{i}")
            
            # Search operations
            search_results = []
            for i in range(0, 500, 10):
                if f"item_{i}" in data_list:
                    search_results.append(f"item_{i}")
                
                if f"key_{i}" in data_dict:
                    search_results.append(data_dict[f"key_{i}"])
                
                if f"set_item_{i}" in data_set:
                    search_results.append(f"set_item_{i}")
            
            return {
                'list_size': len(data_list),
                'dict_size': len(data_dict),
                'set_size': len(data_set),
                'search_results': len(search_results)
            }

        result = benchmark(data_structure_operations)
        assert result['list_size'] == 500
        assert result['dict_size'] == 500
        assert result['set_size'] == 500

    def test_timing_critical_operations(self, benchmark):
        """Test operations that must complete within time limits."""
        def timing_critical_operation():
            start_time = time.time()
            
            # Simulate time-critical operations
            emails = []
            for i in range(100):
                email = generate_email(f"timing{i}")
                emails.append(email)
                
                # Simulate processing delay
                time.sleep(0.001)  # 1ms delay per operation
            
            end_time = time.time()
            duration = end_time - start_time
            
            return {
                'emails_generated': len(emails),
                'duration': duration,
                'avg_time_per_email': duration / len(emails) if emails else 0
            }

        result = benchmark(timing_critical_operation)
        assert result['emails_generated'] == 100
        # Ensure average time per email is reasonable (less than 10ms)
        assert result['avg_time_per_email'] < 0.01


@pytest.mark.performance
class TestPerformanceRegression:
    """Performance regression tests."""

    def test_no_performance_regression_email_generation(self, benchmark):
        """Ensure email generation doesn't regress in performance."""
        def generate_emails():
            return [generate_email(f"regression{i}") for i in range(50)]

        result = benchmark(generate_emails)
        assert len(result) == 50
        
        # Performance assertion: should complete in reasonable time
        # This will fail if performance significantly degrades
        assert benchmark.stats.stats.mean < 0.1  # Less than 100ms average

    def test_no_memory_leak_in_operations(self, benchmark):
        """Test for memory leaks in repeated operations."""
        import gc
        
        def repeated_operations():
            gc.collect()
            initial_objects = len(gc.get_objects())
            
            # Perform operations multiple times
            for _ in range(100):
                email = generate_email("leak_test")
                config = get_config()
                del email, config
            
            gc.collect()
            final_objects = len(gc.get_objects())
            
            return {
                'initial_objects': initial_objects,
                'final_objects': final_objects,
                'object_growth': final_objects - initial_objects
            }

        result = benchmark(repeated_operations)
        
        # Memory leak check: object growth should be minimal
        assert result['object_growth'] < 100  # Less than 100 new objects
