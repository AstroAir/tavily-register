# Troubleshooting Guide

This comprehensive troubleshooting guide helps you diagnose and resolve common issues with Tavily Register. Use the quick navigation below to find solutions for your specific problem.

## Quick Problem Finder

<div class="grid cards" markdown>

-   :material-alert-circle:{ .lg .middle } **Common Issues**

    ---

    Most frequently encountered problems and solutions

    [:octicons-arrow-right-24: Common Issues](common-issues.md)

-   :material-message-alert:{ .lg .middle } **Error Messages**

    ---

    Specific error messages and their meanings

    [:octicons-arrow-right-24: Error Messages](error-messages.md)

-   :material-speedometer:{ .lg .middle } **Performance Issues**

    ---

    Optimization tips and performance troubleshooting

    [:octicons-arrow-right-24: Performance Tips](performance.md)

</div>

## Diagnostic Tools

### Quick Health Check

Run this command to check your installation:

```bash
python -c "
import sys
print(f'Python version: {sys.version}')

try:
    from src.tavily_register.main import main
    print('✅ Tavily Register imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')

try:
    from playwright.sync_api import sync_playwright
    print('✅ Playwright available')
except ImportError:
    print('❌ Playwright not installed')

try:
    from src.tavily_register.config.settings import EMAIL_PREFIX, BROWSER_TYPE
    print(f'✅ Configuration loaded: {EMAIL_PREFIX}, {BROWSER_TYPE}')
except Exception as e:
    print(f'❌ Configuration error: {e}')
"
```

### System Information

Gather system information for bug reports:

```bash
python -c "
import platform
import sys
import subprocess

print('=== System Information ===')
print(f'OS: {platform.system()} {platform.release()}')
print(f'Python: {sys.version}')
print(f'Architecture: {platform.machine()}')

try:
    result = subprocess.run(['playwright', '--version'], capture_output=True, text=True)
    print(f'Playwright: {result.stdout.strip()}')
except:
    print('Playwright: Not available')

try:
    import pkg_resources
    packages = ['playwright', 'beautifulsoup4', 'requests', 'lxml']
    for pkg in packages:
        try:
            version = pkg_resources.get_distribution(pkg).version
            print(f'{pkg}: {version}')
        except:
            print(f'{pkg}: Not installed')
except:
    print('Package information not available')
"
```

## Problem Categories

### 🚀 Installation Issues

??? failure "Python Version Too Low"
    
    **Error:** `Python version too low` or compatibility warnings
    
    **Solution:**
    
    1. Check your Python version: `python --version`
    2. Install Python 3.12+ from [python.org](https://python.org)
    3. Use virtual environment: `python3.12 -m venv venv`
    4. Update pip: `python -m pip install --upgrade pip`

??? failure "Playwright Installation Failed"
    
    **Error:** Browser installation fails or Playwright not found
    
    **Solutions:**
    
    ```bash
    # Method 1: Reinstall Playwright
    pip uninstall playwright
    pip install playwright
    playwright install firefox
    
    # Method 2: Install specific browser
    playwright install chromium
    
    # Method 3: System package (Linux)
    sudo apt-get install firefox  # Ubuntu/Debian
    sudo yum install firefox       # CentOS/RHEL
    ```

??? failure "Permission Errors"
    
    **Error:** `PermissionError` or access denied
    
    **Solutions:**
    
    ```bash
    # Use user installation
    pip install --user -e .
    
    # Fix permissions (Linux/Mac)
    chmod +x scripts/setup.py
    
    # Use virtual environment
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

### 📧 Email Configuration Issues

??? failure "Email Login Failed"
    
    **Error:** Cannot login to 2925.com or cookies invalid
    
    **Solutions:**
    
    1. **Clear cookies and retry:**
       ```bash
       rm email_cookies.json
       python main.py  # Choose option 3
       ```
    
    2. **Check email credentials:**
       - Verify 2925.com account is active
       - Try logging in manually first
       - Check for CAPTCHA requirements
    
    3. **Browser compatibility:**
       ```bash
       # Try different browser
       export BROWSER_TYPE=chromium
       python main.py
       ```

??? failure "Email Verification Timeout"
    
    **Error:** Verification email not received or timeout
    
    **Solutions:**
    
    1. **Increase timeout:**
       ```python
       # In settings or .env
       WAIT_TIME_LONG=20
       MAX_TIMEOUT=120
       ```
    
    2. **Check email manually:**
       - Login to 2925.com webmail
       - Look for verification emails
       - Check spam/junk folder
    
    3. **Retry with different prefix:**
       ```bash
       export EMAIL_PREFIX=different_prefix
       python main.py
       ```

### 🌐 Browser Automation Issues

??? failure "Browser Crashes or Hangs"
    
    **Error:** Browser becomes unresponsive or crashes
    
    **Solutions:**
    
    1. **Use headless mode:**
       ```bash
       export HEADLESS=true
       python main.py
       ```
    
    2. **Increase memory:**
       ```bash
       # Close other applications
       # Use lighter browser
       export BROWSER_TYPE=firefox
       ```
    
    3. **Update browser:**
       ```bash
       playwright install --force firefox
       ```

??? failure "Element Not Found"
    
    **Error:** Cannot find form elements or buttons
    
    **Solutions:**
    
    1. **Use test mode for debugging:**
       ```bash
       python main.py  # Choose option 2
       ```
    
    2. **Check website changes:**
       - Website might have updated
       - Try intelligent mode
       - Report issue on GitHub
    
    3. **Adjust wait times:**
       ```python
       WAIT_TIME_MEDIUM=10
       WAIT_TIME_LONG=20
       ```

### 🔧 Configuration Issues

??? failure "Settings Not Loading"
    
    **Error:** Configuration changes not taking effect
    
    **Solutions:**
    
    1. **Check file locations:**
       ```bash
       # Verify .env file exists
       ls -la .env
       
       # Check settings file
       cat src/tavily_register/config/settings.py
       ```
    
    2. **Environment variable priority:**
       ```bash
       # Check current environment
       env | grep EMAIL_PREFIX
       env | grep BROWSER_TYPE
       ```
    
    3. **Restart application:**
       - Configuration is loaded at startup
       - Restart after making changes

??? failure "Invalid Email Prefix"
    
    **Error:** Email generation fails or invalid format
    
    **Solutions:**
    
    1. **Use valid characters:**
       ```bash
       # Good examples
       EMAIL_PREFIX=user123
       EMAIL_PREFIX=project_alpha
       EMAIL_PREFIX=test_env
       
       # Avoid special characters
       # EMAIL_PREFIX=user@123  # Bad
       # EMAIL_PREFIX=user.123  # Bad
       ```
    
    2. **Check length limits:**
       - Keep prefix between 3-20 characters
       - Avoid very long prefixes

## Debug Mode

Enable debug mode for detailed troubleshooting:

```bash
# Set debug environment
export DEBUG=true
export LOG_LEVEL=DEBUG
export SAVE_SCREENSHOTS=true

# Run with debug output
python main.py
```

Debug mode provides:

- **Detailed logs** of each step
- **Screenshots** on errors
- **HTML dumps** for analysis
- **Timing information** for performance
- **Network request** logging

## Log Analysis

### Understanding Log Levels

| Level | Description | When to Use |
|-------|-------------|-------------|
| `DEBUG` | Detailed execution info | Development, troubleshooting |
| `INFO` | General information | Normal operation |
| `WARNING` | Potential issues | Monitoring |
| `ERROR` | Error conditions | Problem diagnosis |
| `CRITICAL` | Serious errors | System failures |

### Common Log Patterns

**Success Patterns:**
```
INFO: Starting automation...
INFO: Browser started successfully
INFO: Registration form filled
INFO: Email verification completed
INFO: API key extracted: tvly-dev-xxxxxxxxxx
```

**Warning Patterns:**
```
WARNING: Retrying element detection...
WARNING: Slow page load detected
WARNING: Email verification taking longer than expected
```

**Error Patterns:**
```
ERROR: Browser failed to start
ERROR: Element not found: #submit-button
ERROR: Network timeout
ERROR: Email verification failed
```

## Performance Optimization

### Memory Usage

Monitor and optimize memory usage:

```python
import psutil
import os

def check_memory():
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Memory usage: {memory_mb:.1f} MB")

# Use during automation
check_memory()
```

### Browser Optimization

```bash
# Use headless mode for better performance
export HEADLESS=true

# Reduce browser features
export BROWSER_ARGS="--no-sandbox --disable-dev-shm-usage"

# Use faster browser
export BROWSER_TYPE=chromium
```

## Getting Help

### Before Reporting Issues

1. **Check this troubleshooting guide**
2. **Search existing issues** on GitHub
3. **Try debug mode** to gather more information
4. **Test with minimal configuration**

### Reporting Bugs

Include this information in bug reports:

```bash
# System information
python --version
uname -a  # Linux/Mac
systeminfo  # Windows

# Package versions
pip list | grep -E "(playwright|beautifulsoup4|requests)"

# Configuration (sanitized)
echo "EMAIL_PREFIX: ${EMAIL_PREFIX:-not_set}"
echo "BROWSER_TYPE: ${BROWSER_TYPE:-not_set}"
echo "HEADLESS: ${HEADLESS:-not_set}"

# Error logs
tail -50 logs/tavily_register.log
```

### Community Support

- 🐛 [GitHub Issues](https://github.com/yatotm/tavily-register/issues) - Bug reports
- 💬 [Discussions](https://github.com/yatotm/tavily-register/discussions) - Questions
- 📧 [Email Support](mailto:support@tavily-register.com) - Direct help

## Emergency Recovery

### Complete Reset

If everything fails, try a complete reset:

```bash
# 1. Backup important data
cp api_keys.md api_keys_backup.md
cp email_cookies.json email_cookies_backup.json

# 2. Clean installation
rm -rf venv/
rm email_cookies.json
rm -rf __pycache__/
rm -rf site/

# 3. Fresh install
python -m venv venv
source venv/bin/activate
pip install -e .
playwright install firefox

# 4. Reconfigure
cp .env.example .env
# Edit .env with your settings

# 5. Test
python main.py
```

### Rollback to Previous Version

```bash
# Check available versions
git tag

# Rollback to stable version
git checkout v0.1.0

# Reinstall
pip install -e .
```

## Prevention Tips

1. **Regular Updates:** Keep dependencies updated
2. **Backup Configuration:** Save working configurations
3. **Monitor Logs:** Check logs regularly for warnings
4. **Test Changes:** Test configuration changes in development
5. **Document Issues:** Keep notes of solutions that work

Remember: Most issues are configuration-related and can be resolved by carefully checking settings and following the troubleshooting steps above.
