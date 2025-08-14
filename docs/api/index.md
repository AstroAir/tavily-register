# API Reference

Welcome to the Tavily Register API documentation. This section provides comprehensive reference material for all classes, methods, and functions in the Tavily Register library.

## Overview

The Tavily Register API is organized into several key modules:

<div class="grid cards" markdown>

-   :material-cog:{ .lg .middle } **Core Modules**

    ---

    Main automation classes and intelligent processing

    [:octicons-arrow-right-24: Core API](core.md)

-   :material-email:{ .lg .middle } **Email Modules**

    ---

    Email verification and authentication handling

    [:octicons-arrow-right-24: Email API](email.md)

-   :material-settings:{ .lg .middle } **Configuration**

    ---

    Settings, constants, and configuration management

    [:octicons-arrow-right-24: Configuration API](configuration.md)

-   :material-tools:{ .lg .middle } **Utilities**

    ---

    Helper functions and utility classes

    [:octicons-arrow-right-24: Utilities API](utilities.md)

</div>

## Quick Reference

### Main Classes

| Class | Module | Description |
|-------|--------|-------------|
| `IntelligentTavilyAutomation` | `core.intelligent_automation` | Advanced automation with intelligent element detection |
| `TavilyAutomation` | `core.traditional_automation` | Traditional automation approach for testing |
| `TavilyMainController` | `main` | Main application controller and user interface |
| `EmailChecker` | `email.checker` | Email verification and checking functionality |
| `EmailLoginHelper` | `email.login_helper` | Email login assistance and cookie management |

### Key Functions

| Function | Module | Description |
|----------|--------|-------------|
| `main()` | `main` | Main entry point for the application |
| `generate_email()` | `utils.helpers` | Generate unique email addresses |
| `save_api_key()` | `utils.helpers` | Save API keys to file |
| `load_cookies()` | `utils.helpers` | Load email authentication cookies |

## Usage Patterns

### Basic Usage

```python
from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation

# Create automation instance
automation = IntelligentTavilyAutomation()

# Run complete automation
success = automation.run_automation()

if success:
    print(f"API Key: {automation.api_key}")
    print(f"Email: {automation.email}")
```

### Advanced Usage

```python
from src.tavily_register.main import TavilyMainController
from src.tavily_register.config.settings import *

# Create controller with custom settings
controller = TavilyMainController()

# Set custom email prefix
controller.email_prefix = "custom_prefix"

# Run intelligent mode
controller.run_intelligent_mode()
```

### Email Management

```python
from src.tavily_register.email.checker import EmailChecker
from src.tavily_register.email.login_helper import EmailLoginHelper

# Setup email authentication
login_helper = EmailLoginHelper()
login_helper.setup_email_login()

# Check for verification emails
checker = EmailChecker("user@2925.com")
verification_link = checker.get_verification_link()
```

## Error Handling

All API methods use consistent error handling patterns:

```python
try:
    automation = IntelligentTavilyAutomation()
    result = automation.run_automation()
except Exception as e:
    print(f"Automation failed: {e}")
    # Handle error appropriately
```

### Common Exceptions

| Exception | Description | Handling |
|-----------|-------------|----------|
| `BrowserError` | Browser automation failures | Retry with different browser |
| `EmailError` | Email verification issues | Check email configuration |
| `NetworkError` | Network connectivity problems | Verify internet connection |
| `ConfigurationError` | Invalid configuration settings | Check settings file |

## Type Hints

The API uses comprehensive type hints for better development experience:

```python
from typing import Optional, Tuple, Dict, Any

def run_automation(self) -> bool:
    """Run complete automation workflow.
    
    Returns:
        bool: True if successful, False otherwise
    """
    pass

def get_api_key(self) -> Optional[str]:
    """Extract API key from page.
    
    Returns:
        Optional[str]: API key if found, None otherwise
    """
    pass
```

## Configuration

### Environment Variables

The API respects these environment variables:

```python
# Email configuration
EMAIL_PREFIX: str = "user123"
EMAIL_DOMAIN: str = "2925.com"

# Browser configuration
BROWSER_TYPE: str = "firefox"  # or "chromium"
HEADLESS: bool = False

# Timing configuration
WAIT_TIME_SHORT: int = 2
WAIT_TIME_MEDIUM: int = 5
WAIT_TIME_LONG: int = 10

# Debug configuration
DEBUG: bool = False
LOG_LEVEL: str = "INFO"
```

### Settings Override

```python
from src.tavily_register.config import settings

# Override settings programmatically
settings.BROWSER_TYPE = "chromium"
settings.HEADLESS = True
settings.WAIT_TIME_MEDIUM = 8
```

## Logging

The API provides comprehensive logging:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Use in your code
logger = logging.getLogger(__name__)
logger.info("Starting automation...")
```

## Testing

### Unit Testing

```python
import pytest
from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation

def test_automation_initialization():
    automation = IntelligentTavilyAutomation()
    assert automation is not None
    assert automation.email_prefix is not None

@pytest.mark.integration
def test_full_automation():
    automation = IntelligentTavilyAutomation()
    # Note: This requires actual browser and network access
    result = automation.run_automation()
    assert isinstance(result, bool)
```

### Mocking

```python
from unittest.mock import Mock, patch

@patch('src.tavily_register.core.intelligent_automation.sync_playwright')
def test_automation_with_mock(mock_playwright):
    mock_browser = Mock()
    mock_playwright.return_value.__enter__.return_value.firefox.launch.return_value = mock_browser
    
    automation = IntelligentTavilyAutomation()
    # Test with mocked browser
```

## Performance Considerations

### Memory Management

```python
# Always close browser instances
automation = IntelligentTavilyAutomation()
try:
    result = automation.run_automation()
finally:
    automation.close_browser()
```

### Async Support

For high-performance scenarios, consider using async patterns:

```python
import asyncio
from playwright.async_api import async_playwright

async def run_multiple_automations():
    tasks = []
    for i in range(5):
        task = asyncio.create_task(run_single_automation(f"prefix_{i}"))
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results
```

## Migration Guide

### From v0.1.0 to v0.2.0

```python
# Old way (v0.1.0)
from tavily_automation import TavilyAutomation
automation = TavilyAutomation()

# New way (v0.2.0+)
from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation
automation = IntelligentTavilyAutomation()
```

## Contributing to the API

When contributing new API methods:

1. **Follow naming conventions**: Use clear, descriptive names
2. **Add type hints**: Include comprehensive type annotations
3. **Write docstrings**: Use Google-style docstrings
4. **Add tests**: Include unit and integration tests
5. **Update documentation**: Keep this reference up to date

## Support

For API-related questions:

- 📖 [User Guide](../user-guide/index.md) - Usage examples and tutorials
- 🐛 [Issue Tracker](https://github.com/yatotm/tavily-register/issues) - Report bugs
- 💬 [Discussions](https://github.com/yatotm/tavily-register/discussions) - Ask questions
- 📧 [Email Support](mailto:support@tavily-register.com) - Direct support
