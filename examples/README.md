# Examples Directory

This directory contains usage examples and sample code for the Tavily Register application.

## Examples

- **basic_usage.py**: Basic usage example showing simple registration
- **advanced_usage.py**: Advanced usage with custom configuration

## Usage

### Basic Example
```bash
python examples/basic_usage.py
```

Shows how to:
- Import the main modules
- Configure basic settings
- Run a simple registration

### Advanced Example
```bash
python examples/advanced_usage.py
```

Demonstrates:
- Custom configuration
- Error handling
- Multiple registrations
- Advanced automation features

## Learning Path

1. **Start with `basic_usage.py`** to understand the fundamentals
2. **Review `advanced_usage.py`** for more complex scenarios
3. **Refer to the main documentation** for complete API reference

## Prerequisites

Before running examples:
```bash
# Install the package
pip install -e .

# Configure your email prefix
cp .env.example .env
# Edit .env with your EMAIL_PREFIX

# Ensure Playwright browsers are installed
playwright install firefox
```

## Example Guidelines

Examples in this directory:
1. **Are self-contained** and can run independently
2. **Include comprehensive comments** explaining each step
3. **Demonstrate best practices** for using the automation system
4. **Handle errors gracefully** with proper exception handling
5. **Show realistic use cases** for practical applications

## Common Patterns

### Basic Automation
```python
from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation

automation = IntelligentTavilyAutomation()
try:
    automation.email_prefix = "example"
    automation.start_browser(headless=True)
    api_key = automation.run_complete_automation()
    print(f"Success: {api_key}")
finally:
    automation.close_browser()
```

### Configuration Management
```python
import os
from src.tavily_register.config.settings import EMAIL_PREFIX, BROWSER_TYPE

# Override configuration
os.environ['EMAIL_PREFIX'] = 'custom_prefix'
os.environ['HEADLESS'] = 'true'
```

## Troubleshooting

If examples fail:
1. **Check installation**: `pip list | grep tavily`
2. **Verify configuration**: Check your `.env` file
3. **Browser setup**: Run `playwright install firefox`
4. **Dependencies**: Ensure all requirements are installed
