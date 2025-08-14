# Configuration Guide

This guide covers all configuration options available in Tavily Register, from basic email setup to advanced automation settings.

## Configuration Methods

Tavily Register supports multiple configuration methods, listed in order of precedence:

1. **Environment Variables** (highest priority)
2. **`.env` file** 
3. **Settings file** (`src/tavily_register/config/settings.py`)
4. **Default values** (lowest priority)

## Basic Configuration

### Email Settings

The most important configuration is your email setup:

=== "Environment Variables"

    ```bash
    # Set in your shell or CI/CD environment
    export EMAIL_PREFIX="your_unique_prefix"
    export EMAIL_DOMAIN="2925.com"
    ```

=== ".env File"

    Create a `.env` file in the project root:
    
    ```bash
    # Required: Your unique email prefix
    EMAIL_PREFIX=your_unique_prefix
    
    # Optional: Email domain (default: 2925.com)
    EMAIL_DOMAIN=2925.com
    
    # Generated email will be: your_unique_prefix-random@2925.com
    ```

=== "Settings File"

    Edit `src/tavily_register/config/settings.py`:
    
    ```python
    # Email configuration
    EMAIL_PREFIX = "your_unique_prefix"
    EMAIL_DOMAIN = "2925.com"
    ```

!!! warning "Email Prefix Requirements"
    - Must be **unique** to avoid conflicts
    - Use **alphanumeric characters** only
    - Avoid special characters except hyphens and underscores
    - Keep it **memorable** for easy identification

### Browser Configuration

Configure browser behavior for automation:

```bash
# Browser type: firefox (recommended) or chromium
BROWSER_TYPE=firefox

# Headless mode: true for background operation, false for visible browser
HEADLESS=false

# Browser timeout in seconds
BROWSER_TIMEOUT=30
```

### Timing Configuration

Adjust wait times for different operations:

```bash
# Short operations (button clicks, form fills)
WAIT_TIME_SHORT=2

# Medium operations (page loads, form submissions)
WAIT_TIME_MEDIUM=5

# Long operations (email verification, complex page loads)
WAIT_TIME_LONG=10

# Maximum timeout for critical operations
MAX_TIMEOUT=60
```

## Advanced Configuration

### Debug and Logging

Enable detailed logging and debugging:

```bash
# Enable debug mode
DEBUG=true

# Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# Save screenshots on errors
SAVE_SCREENSHOTS=true

# Screenshot directory
SCREENSHOT_DIR=screenshots

# Enable HTML logging (test mode)
HTML_LOGGING=true
```

### Network Configuration

Configure network-related settings:

```bash
# Request timeout in seconds
REQUEST_TIMEOUT=30

# Maximum retries for network operations
MAX_RETRIES=3

# Retry delay in seconds
RETRY_DELAY=2

# User agent string (optional)
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```

### File Paths

Customize file locations:

```bash
# API keys output file
API_KEYS_FILE=api_keys.md

# Email cookies file
COOKIES_FILE=email_cookies.json

# Log file location
LOG_FILE=logs/tavily_register.log

# Temporary files directory
TEMP_DIR=temp
```

## Configuration Examples

### Development Environment

Perfect for testing and debugging:

```bash
# .env file for development
EMAIL_PREFIX=dev_user
BROWSER_TYPE=firefox
HEADLESS=false
DEBUG=true
LOG_LEVEL=DEBUG
SAVE_SCREENSHOTS=true
WAIT_TIME_SHORT=3
WAIT_TIME_MEDIUM=7
WAIT_TIME_LONG=15
HTML_LOGGING=true
```

### Production Environment

Optimized for performance and reliability:

```bash
# .env file for production
EMAIL_PREFIX=prod_user
BROWSER_TYPE=firefox
HEADLESS=true
DEBUG=false
LOG_LEVEL=INFO
SAVE_SCREENSHOTS=false
WAIT_TIME_SHORT=2
WAIT_TIME_MEDIUM=5
WAIT_TIME_LONG=10
MAX_RETRIES=5
```

### CI/CD Environment

Configuration for automated testing:

```bash
# .env file for CI/CD
EMAIL_PREFIX=ci_test
BROWSER_TYPE=chromium
HEADLESS=true
DEBUG=false
LOG_LEVEL=WARNING
SAVE_SCREENSHOTS=true
WAIT_TIME_SHORT=1
WAIT_TIME_MEDIUM=3
WAIT_TIME_LONG=8
MAX_TIMEOUT=30
```

## Configuration Validation

### Checking Current Configuration

```python
from src.tavily_register.config.settings import *

# Print current configuration
print(f"Email Prefix: {EMAIL_PREFIX}")
print(f"Browser Type: {BROWSER_TYPE}")
print(f"Headless Mode: {HEADLESS}")
print(f"Debug Mode: {DEBUG}")
```

### Validation Script

Create a validation script to check your configuration:

```python
#!/usr/bin/env python3
"""Configuration validation script."""

import os
from src.tavily_register.config.settings import *

def validate_config():
    """Validate current configuration."""
    issues = []
    
    # Check email prefix
    if not EMAIL_PREFIX or EMAIL_PREFIX == "user123":
        issues.append("❌ EMAIL_PREFIX not set or using default value")
    elif not EMAIL_PREFIX.replace('_', '').replace('-', '').isalnum():
        issues.append("❌ EMAIL_PREFIX contains invalid characters")
    else:
        print(f"✅ Email prefix: {EMAIL_PREFIX}")
    
    # Check browser type
    if BROWSER_TYPE not in ["firefox", "chromium"]:
        issues.append(f"❌ Invalid BROWSER_TYPE: {BROWSER_TYPE}")
    else:
        print(f"✅ Browser type: {BROWSER_TYPE}")
    
    # Check timing values
    if WAIT_TIME_SHORT >= WAIT_TIME_MEDIUM:
        issues.append("❌ WAIT_TIME_SHORT should be less than WAIT_TIME_MEDIUM")
    if WAIT_TIME_MEDIUM >= WAIT_TIME_LONG:
        issues.append("❌ WAIT_TIME_MEDIUM should be less than WAIT_TIME_LONG")
    
    if not issues:
        print("✅ Configuration validation passed!")
        return True
    else:
        print("Configuration issues found:")
        for issue in issues:
            print(f"  {issue}")
        return False

if __name__ == "__main__":
    validate_config()
```

## Environment-Specific Setup

### Docker Configuration

For containerized deployments:

```dockerfile
# Dockerfile environment variables
ENV EMAIL_PREFIX=docker_user
ENV BROWSER_TYPE=chromium
ENV HEADLESS=true
ENV DEBUG=false
```

### Kubernetes Configuration

Using ConfigMaps and Secrets:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: tavily-config
data:
  BROWSER_TYPE: "chromium"
  HEADLESS: "true"
  DEBUG: "false"
  LOG_LEVEL: "INFO"
---
apiVersion: v1
kind: Secret
metadata:
  name: tavily-secrets
type: Opaque
stringData:
  EMAIL_PREFIX: "k8s_user"
```

### GitHub Actions Configuration

For CI/CD pipelines:

```yaml
env:
  EMAIL_PREFIX: ${{ secrets.EMAIL_PREFIX }}
  BROWSER_TYPE: chromium
  HEADLESS: true
  DEBUG: false
  SAVE_SCREENSHOTS: true
```

## Troubleshooting Configuration

### Common Issues

??? failure "Configuration Not Loading"
    
    **Problem:** Changes to configuration are not taking effect.
    
    **Solutions:**
    
    1. Check file locations and permissions
    2. Verify environment variable names (case-sensitive)
    3. Restart the application after changes
    4. Use absolute paths for file configurations

??? failure "Invalid Email Prefix"
    
    **Problem:** Email generation fails or produces invalid addresses.
    
    **Solutions:**
    
    1. Use only alphanumeric characters, hyphens, and underscores
    2. Avoid starting with numbers or special characters
    3. Keep prefix length between 3-20 characters
    4. Test with a simple prefix first

??? failure "Browser Configuration Issues"
    
    **Problem:** Browser fails to start or behaves unexpectedly.
    
    **Solutions:**
    
    1. Install browser: `playwright install firefox`
    2. Try different browser type: `BROWSER_TYPE=chromium`
    3. Check headless mode setting
    4. Verify system permissions

### Configuration Testing

Test your configuration before running automation:

```bash
# Test configuration
python -c "
from src.tavily_register.config.settings import *
from src.tavily_register.utils.helpers import generate_email

print('Testing configuration...')
email = generate_email()
print(f'Generated email: {email}')
print('Configuration test passed!')
"
```

## Best Practices

1. **Use environment variables** for sensitive or environment-specific settings
2. **Keep `.env` files** out of version control (add to `.gitignore`)
3. **Document custom configurations** for team members
4. **Test configurations** in development before production deployment
5. **Use validation scripts** to catch configuration errors early
6. **Monitor logs** to identify configuration-related issues

## Next Steps

After configuring Tavily Register:

- 📚 [Quick Start Guide](quick-start.md) - Run your first automation
- 🔧 [User Guide](../user-guide/index.md) - Learn advanced features
- 🐛 [Troubleshooting](../troubleshooting/index.md) - Solve common issues
