# Comprehensive Test Suite

This directory contains a comprehensive test suite for the Tavily Register project, providing extensive coverage across all modules and scenarios.

## 🎯 Test Coverage Overview

The enhanced test suite now provides comprehensive coverage for:

### ✅ Core Automation Classes
- **IntelligentTavilyAutomation** - Complete browser automation workflow
- **TavilyAutomation** - Traditional automation with HTML collection
- **EmailChecker** - Email verification and link extraction
- **EmailLoginHelper** - Cookie management and login guidance
- **TavilyMainController** - Main application controller and menu system

### ✅ Utility Functions
- **Configuration Management** - Environment variables, type conversion, validation
- **File Operations** - API key storage, cookie management, error handling
- **Email Generation** - Random suffix generation, email formatting
- **Logging and Debugging** - Action logging, timing mechanisms

### ✅ Integration Scenarios
- **End-to-End Workflows** - Complete automation from start to finish
- **Component Integration** - Inter-module communication and data flow
- **Error Recovery** - Retry mechanisms and graceful failure handling
- **Resource Management** - Browser lifecycle and cleanup

### ✅ Edge Cases and Error Handling
- **Boundary Conditions** - Empty inputs, extreme values, malformed data
- **Network Failures** - Timeouts, connection errors, browser crashes
- **File System Errors** - Permission denied, disk full, corrupted files
- **Configuration Issues** - Invalid values, missing settings, type errors

### ✅ Performance and Concurrency
- **Performance Testing** - Timing validation, memory usage, bulk operations
- **Concurrent Operations** - Multi-threading, resource contention
- **Timeout Handling** - Proper timeout management and recovery

## 📁 Directory Structure

```
tests/
├── unit/                           # Unit tests for individual modules
│   ├── test_config.py             # Configuration management tests
│   ├── test_utils.py              # Utility function tests (enhanced)
│   ├── test_intelligent_automation.py  # Intelligent automation tests
│   ├── test_traditional_automation.py  # Traditional automation tests
│   ├── test_email_checker.py      # Email verification tests
│   ├── test_email_login_helper.py # Email login helper tests
│   └── test_main_controller.py    # Main controller tests
├── integration/                    # Integration and workflow tests
│   └── test_basic_workflow.py     # Enhanced integration scenarios
├── fixtures/                      # Test fixtures and sample data
│   └── sample_data.py             # Comprehensive test data
└── run_comprehensive_tests.py     # Test runner with coverage analysis
```

## 🚀 Running Tests

### Quick Start
```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock

# Run comprehensive test suite
python tests/run_comprehensive_tests.py

# Run all tests with coverage
pytest --cov=src --cov-report=html --cov-report=term-missing
```

### Detailed Test Commands

```bash
# Run specific test categories
pytest tests/unit/ -v                    # Unit tests only
pytest tests/integration/ -v             # Integration tests only

# Run specific module tests
pytest tests/unit/test_intelligent_automation.py -v
pytest tests/unit/test_email_checker.py -v
pytest tests/unit/test_main_controller.py -v

# Run tests by keyword
pytest -k "error" -v                     # Error handling tests
pytest -k "performance" -v               # Performance tests
pytest -k "integration" -v               # Integration tests
pytest -k "boundary" -v                  # Boundary condition tests

# Run tests with timing information
pytest --durations=10                    # Show 10 slowest tests

# Coverage analysis
pytest --cov=src --cov-report=html       # HTML coverage report
pytest --cov=src --cov-fail-under=80     # Fail if coverage < 80%
```

### Test Categories

The test suite includes several categories of tests:

- **Unit Tests** (`tests/unit/`) - Test individual functions and classes
- **Integration Tests** (`tests/integration/`) - Test component interactions
- **Error Handling Tests** (`-k "error"`) - Test error scenarios and recovery
- **Performance Tests** (`-k "performance"`) - Test timing and resource usage
- **Boundary Tests** (`-k "boundary"`) - Test edge cases and limits

## Test Guidelines

When writing tests:

1. **Descriptive Names**: Use clear, descriptive test function names
2. **AAA Pattern**: Follow Arrange, Act, Assert structure
3. **Independence**: Tests should not depend on each other
4. **Mocking**: Mock external dependencies (browsers, network calls)
5. **Edge Cases**: Test both success and failure scenarios

## Test Configuration

Tests are configured via `pyproject.toml` with the following markers:
- `unit`: Unit tests for individual components
- `integration`: Integration tests for complete workflows
- `slow`: Tests that take longer to execute

## Writing Tests

### Example Test Structure
```python
def test_email_generation():
    # Arrange
    prefix = "test_user"

    # Act
    email = generate_email(prefix)

    # Assert
    assert email.startswith(prefix)
    assert "@2925.com" in email
```

### Mocking External Dependencies
```python
@pytest.fixture
def mock_browser():
    with patch('playwright.sync_api.sync_playwright') as mock:
        yield mock

def test_automation_with_mock(mock_browser):
    # Test automation logic without actual browser
    automation = IntelligentTavilyAutomation()
    # ... test implementation
```

## Test Environment

- Tests run in isolated environments
- External dependencies are mocked
- Browser tests use headless mode
- Temporary files are cleaned up automatically
