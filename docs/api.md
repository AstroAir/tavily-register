# API Reference

This document provides detailed API documentation for the Tavily Register project.

## Core Modules

### IntelligentTavilyAutomation

The main intelligent automation class that handles the complete registration process.

```python
from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation

automation = IntelligentTavilyAutomation()
```

#### Methods

##### `__init__()`

Initialize the automation instance.

```python
automation = IntelligentTavilyAutomation()
```

##### `start_browser(headless=False)`

Start the browser instance.

**Parameters:**
- `headless` (bool): Whether to run in headless mode. Default: False

**Returns:**
- None

**Example:**
```python
automation.start_browser(headless=True)
```

##### `run_complete_automation()`

Execute the complete automation workflow: registration + email verification + API key extraction.

**Returns:**
- `str`: API key if successful, None if failed

**Example:**
```python
api_key = automation.run_complete_automation()
if api_key:
    print(f"Success! API Key: {api_key}")
```

##### `run_registration()`

Execute only the registration phase.

**Returns:**
- `bool`: True if registration successful, False otherwise

##### `close_browser()`

Close the browser instance and cleanup resources.

**Returns:**
- None

#### Properties

##### `email`

The generated email address for the current registration.

**Type:** `str`

##### `password`

The password used for registration.

**Type:** `str`

##### `email_prefix`

The email prefix used for generating email addresses.

**Type:** `str`

### TavilyAutomation

Traditional automation class for testing and comparison.

```python
from src.tavily_register.core.traditional_automation import TavilyAutomation

automation = TavilyAutomation()
```

#### Methods

Similar to `IntelligentTavilyAutomation` but uses traditional waiting mechanisms.

##### `save_html_log(filename)`

Save HTML information for analysis.

**Parameters:**
- `filename` (str): Output filename for HTML log

**Example:**
```python
automation.save_html_log("debug_log.json")
```

### EmailChecker

Email verification and management class.

```python
from src.tavily_register.email.checker import EmailChecker

checker = EmailChecker()
```

#### Methods

##### `load_email_page()`

Load the email service page.

**Returns:**
- `bool`: True if successful

##### `check_for_tavily_email(email_address)`

Check for Tavily verification emails.

**Parameters:**
- `email_address` (str): Email address to check

**Returns:**
- `str`: Verification link if found, None otherwise

##### `navigate_to_verification_link(link)`

Navigate to the verification link.

**Parameters:**
- `link` (str): Verification URL

**Returns:**
- `str`: Result status ("success", "login_required", etc.)

### EmailLoginHelper

Email login assistance and cookie management.

```python
from src.tavily_register.email.login_helper import EmailLoginHelper

helper = EmailLoginHelper()
```

#### Methods

##### `start_browser()`

Start browser for email login.

##### `save_cookies()`

Save email authentication cookies.

**Returns:**
- `bool`: True if successful

##### `load_cookies()`

Load saved email cookies.

**Returns:**
- `list`: Cookie data if available

## Utility Functions

### Email Generation

```python
from src.tavily_register.utils.helpers import generate_email

# Generate random email
email = generate_email()

# Generate with custom prefix
email = generate_email("custom_prefix")
```

### API Key Storage

```python
from src.tavily_register.utils.helpers import save_api_key

save_api_key(email="test@example.com", api_key="tvly-xxx", password="pass123")
```

### Cookie Management

```python
from src.tavily_register.utils.helpers import save_cookies, load_cookies

# Save cookies
save_cookies(cookie_data, "cookies.json")

# Load cookies
cookies = load_cookies("cookies.json")
```

### Utility Functions

```python
from src.tavily_register.utils.helpers import (
    wait_with_message,
    take_screenshot,
    log_action
)

# Wait with message
wait_with_message(5, "Processing registration")

# Take screenshot
take_screenshot(page, "debug.png")

# Log action
log_action("Registration started", "Email: test@example.com")
```

## Configuration

### Settings Module

```python
from src.tavily_register.config.settings import *

# Access configuration values
print(f"Email domain: {EMAIL_DOMAIN}")
print(f"Browser type: {BROWSER_TYPE}")
print(f"Headless mode: {HEADLESS}")
```

### Environment Variables

All configuration can be overridden using environment variables:

```python
import os

# Set environment variable
os.environ['EMAIL_PREFIX'] = 'new_prefix'

# Configuration will automatically use the new value
from src.tavily_register.config.settings import EMAIL_PREFIX
print(EMAIL_PREFIX)  # Output: 'new_prefix'
```

## Main Controller

### TavilyMainController

The main application controller that manages the user interface and workflow.

```python
from src.tavily_register.main import TavilyMainController

controller = TavilyMainController()
controller.run()
```

#### Methods

##### `run()`

Start the main application loop with interactive menu.

##### `run_intelligent_mode()`

Execute intelligent automation mode.

##### `run_test_mode()`

Execute test mode with HTML logging.

##### `setup_email_cookies()`

Interactive email cookie setup.

**Returns:**
- `bool`: True if setup successful

## Error Handling

### Common Exceptions

```python
try:
    automation = IntelligentTavilyAutomation()
    automation.start_browser()
    api_key = automation.run_complete_automation()
except Exception as e:
    print(f"Automation failed: {e}")
finally:
    automation.close_browser()
```

### Best Practices

1. **Always close browsers** in finally blocks
2. **Handle timeouts** gracefully
3. **Log errors** for debugging
4. **Validate inputs** before processing

## Examples

### Complete Automation Example

```python
from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation

def register_account(email_prefix="test", headless=True):
    automation = IntelligentTavilyAutomation()
    
    try:
        # Configure
        automation.email_prefix = email_prefix
        
        # Start browser
        automation.start_browser(headless=headless)
        
        # Run automation
        api_key = automation.run_complete_automation()
        
        if api_key:
            print(f"Success! Email: {automation.email}")
            print(f"API Key: {api_key}")
            return api_key
        else:
            print("Registration failed")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        automation.close_browser()

# Usage
api_key = register_account("myproject", headless=True)
```

### Batch Registration Example

```python
def register_multiple_accounts(count=5, prefix="batch"):
    results = []
    
    for i in range(count):
        print(f"Registering account {i+1}/{count}")
        api_key = register_account(f"{prefix}_{i}", headless=True)
        
        if api_key:
            results.append(api_key)
        
        # Brief pause between registrations
        time.sleep(2)
    
    print(f"Successfully registered {len(results)}/{count} accounts")
    return results
```

## Type Hints

The codebase uses type hints for better code documentation:

```python
from typing import Optional, List, Dict, Union

def generate_email(prefix: Optional[str] = None) -> str:
    """Generate email with optional prefix."""
    pass

def save_api_key(email: str, api_key: str, password: Optional[str] = None) -> None:
    """Save API key information."""
    pass
```
