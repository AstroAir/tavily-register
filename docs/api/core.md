# Core Modules API

The core modules provide the main automation functionality for Tavily Register. These modules handle browser automation, intelligent element detection, and the complete registration workflow.

## IntelligentTavilyAutomation

::: src.tavily_register.core.intelligent_automation.IntelligentTavilyAutomation

The primary automation class that uses advanced HTML analysis and intelligent element detection for optimal performance.

### Class Overview

```python
from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation

# Initialize automation
automation = IntelligentTavilyAutomation()

# Run complete workflow
success = automation.run_automation()
```

### Constructor

#### `__init__(email_prefix: Optional[str] = None)`

Initialize the automation instance with optional email prefix.

**Parameters:**

- `email_prefix` (Optional[str]): Custom email prefix. If None, uses default from settings.

**Example:**

```python
# Use default prefix from settings
automation = IntelligentTavilyAutomation()

# Use custom prefix
automation = IntelligentTavilyAutomation(email_prefix="custom_user")
```

### Browser Management

#### `start_browser(headless: bool = False) -> None`

Start the browser instance with specified configuration.

**Parameters:**

- `headless` (bool): Run browser in headless mode. Default: False

**Raises:**

- `BrowserError`: If browser fails to start

**Example:**

```python
# Start visible browser
automation.start_browser(headless=False)

# Start headless browser
automation.start_browser(headless=True)
```

#### `close_browser() -> None`

Close the browser instance and cleanup resources.

**Example:**

```python
try:
    automation.start_browser()
    # ... automation logic
finally:
    automation.close_browser()
```

### Automation Workflows

#### `run_automation() -> bool`

Execute the complete automation workflow including registration, email verification, and API key extraction.

**Returns:**

- `bool`: True if successful, False otherwise

**Workflow Steps:**

1. Generate unique email address
2. Navigate to Tavily registration page
3. Fill registration form
4. Verify email address
5. Complete login process
6. Extract API key
7. Save results to file

**Example:**

```python
automation = IntelligentTavilyAutomation()
try:
    success = automation.run_automation()
    if success:
        print(f"✅ Success! API Key: {automation.api_key}")
        print(f"📧 Email: {automation.email}")
    else:
        print("❌ Automation failed")
finally:
    automation.close_browser()
```

#### `run_registration() -> bool`

Execute only the registration phase of the automation.

**Returns:**

- `bool`: True if registration successful, False otherwise

**Example:**

```python
# Run only registration
success = automation.run_registration()
if success:
    print("Registration completed successfully")
```

#### `run_email_verification() -> bool`

Execute only the email verification phase.

**Returns:**

- `bool`: True if verification successful, False otherwise

**Example:**

```python
# Assuming registration is already complete
success = automation.run_email_verification()
if success:
    print("Email verified successfully")
```

#### `run_api_extraction() -> Optional[str]`

Execute only the API key extraction phase.

**Returns:**

- `Optional[str]`: API key if found, None otherwise

**Example:**

```python
# Extract API key from current page
api_key = automation.run_api_extraction()
if api_key:
    print(f"API Key extracted: {api_key}")
```

### Properties

#### `email: str`

The generated email address for the current automation session.

```python
automation = IntelligentTavilyAutomation()
print(f"Generated email: {automation.email}")
```

#### `password: str`

The password used for registration.

```python
print(f"Password: {automation.password}")
```

#### `api_key: Optional[str]`

The extracted API key (available after successful automation).

```python
if automation.api_key:
    print(f"API Key: {automation.api_key}")
```

#### `email_prefix: str`

The email prefix used for generating email addresses.

```python
print(f"Email prefix: {automation.email_prefix}")
```

### Advanced Methods

#### `wait_for_element(selector: str, timeout: int = 30) -> bool`

Wait for an element to appear on the page.

**Parameters:**

- `selector` (str): CSS selector for the element
- `timeout` (int): Maximum wait time in seconds

**Returns:**

- `bool`: True if element found, False if timeout

**Example:**

```python
# Wait for submit button
if automation.wait_for_element("button[type='submit']", timeout=10):
    print("Submit button found")
```

#### `intelligent_click(selector: str) -> bool`

Perform intelligent click with retry logic and error handling.

**Parameters:**

- `selector` (str): CSS selector for the element to click

**Returns:**

- `bool`: True if click successful, False otherwise

**Example:**

```python
# Intelligent click with automatic retries
success = automation.intelligent_click("#submit-button")
```

#### `smart_fill_form(form_data: Dict[str, str]) -> bool`

Fill form fields using intelligent field detection.

**Parameters:**

- `form_data` (Dict[str, str]): Mapping of field names to values

**Returns:**

- `bool`: True if form filled successfully, False otherwise

**Example:**

```python
form_data = {
    "email": "user@example.com",
    "password": "secure_password",
    "confirm_password": "secure_password"
}
success = automation.smart_fill_form(form_data)
```

## TavilyAutomation

::: src.tavily_register.core.traditional_automation.TavilyAutomation

Traditional automation class for testing and comparison purposes.

### Class Overview

```python
from src.tavily_register.core.traditional_automation import TavilyAutomation

# Initialize traditional automation
automation = TavilyAutomation()

# Run automation
success = automation.run_automation()
```

### Key Differences from IntelligentTavilyAutomation

| Feature | IntelligentTavilyAutomation | TavilyAutomation |
|---------|----------------------------|------------------|
| Element Detection | Advanced AI-based | Basic CSS selectors |
| Error Handling | Intelligent retry logic | Simple retry |
| Performance | Optimized (95%+ success) | Standard (70-80% success) |
| Debugging | Minimal logging | Extensive HTML logging |
| Use Case | Production | Testing/Debugging |

### Methods

The `TavilyAutomation` class provides similar methods to `IntelligentTavilyAutomation` but with traditional implementation:

- `run_automation() -> bool`
- `run_registration() -> bool`
- `start_browser(headless: bool = False) -> None`
- `close_browser() -> None`

## Error Handling

### Exception Types

```python
from src.tavily_register.core.exceptions import (
    BrowserError,
    ElementNotFoundError,
    TimeoutError,
    AutomationError
)

try:
    automation = IntelligentTavilyAutomation()
    automation.run_automation()
except BrowserError as e:
    print(f"Browser error: {e}")
except ElementNotFoundError as e:
    print(f"Element not found: {e}")
except TimeoutError as e:
    print(f"Operation timed out: {e}")
except AutomationError as e:
    print(f"General automation error: {e}")
```

### Best Practices

1. **Always use try-finally blocks** for browser cleanup:

```python
automation = IntelligentTavilyAutomation()
try:
    result = automation.run_automation()
finally:
    automation.close_browser()
```

2. **Handle specific exceptions** for better error recovery:

```python
try:
    automation.run_automation()
except TimeoutError:
    # Retry with longer timeout
    automation.run_automation()
except BrowserError:
    # Try different browser
    automation.start_browser(headless=True)
    automation.run_automation()
```

3. **Use context managers** for automatic cleanup:

```python
from contextlib import contextmanager

@contextmanager
def automation_context():
    automation = IntelligentTavilyAutomation()
    try:
        automation.start_browser()
        yield automation
    finally:
        automation.close_browser()

# Usage
with automation_context() as automation:
    success = automation.run_automation()
```

## Performance Optimization

### Memory Management

```python
# Efficient resource usage
automation = IntelligentTavilyAutomation()
automation.start_browser(headless=True)  # Use less memory

try:
    # Batch operations
    results = []
    for prefix in ["user1", "user2", "user3"]:
        automation.email_prefix = prefix
        success = automation.run_automation()
        results.append(success)
finally:
    automation.close_browser()  # Clean up once
```

### Concurrent Execution

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def run_single_automation(prefix):
    automation = IntelligentTavilyAutomation(email_prefix=prefix)
    try:
        return automation.run_automation()
    finally:
        automation.close_browser()

# Run multiple automations concurrently
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(run_single_automation, f"user{i}")
        for i in range(5)
    ]
    results = [future.result() for future in futures]
```
