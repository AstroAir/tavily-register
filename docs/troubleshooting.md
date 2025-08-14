# Troubleshooting Guide

This guide helps you resolve common issues when using Tavily Register.

## Installation Issues

### Python Version Errors

**Problem:**
```
Error: Python version too low: 3.11.x
Need Python 3.7 or higher
```

**Solution:**
- Upgrade to Python 3.12 or higher
- Use `python --version` to check your current version
- Download from [python.org](https://python.org) if needed

### Dependency Installation Failures

**Problem:**
```
ERROR: Failed building wheel for playwright
```

**Solutions:**
1. **Update pip first:**
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Install with verbose output:**
   ```bash
   pip install -e . -v
   ```

3. **Try alternative installation:**
   ```bash
   pip install playwright requests beautifulsoup4 lxml
   playwright install firefox
   ```

### Playwright Browser Installation

**Problem:**
```
Error: Failed to install Playwright browsers
```

**Solutions:**
1. **Manual browser installation:**
   ```bash
   playwright install firefox
   ```

2. **Try different browser:**
   ```bash
   playwright install chromium
   # Update BROWSER_TYPE=chromium in .env
   ```

3. **System dependencies (Linux):**
   ```bash
   playwright install-deps
   playwright install firefox
   ```

## Runtime Issues

### Import Errors

**Problem:**
```
ModuleNotFoundError: No module named 'src.tavily_register'
```

**Solutions:**
1. **Install in development mode:**
   ```bash
   pip install -e .
   ```

2. **Check current directory:**
   ```bash
   pwd  # Should be in tavily-register root
   ```

3. **Verify installation:**
   ```bash
   pip list | grep tavily
   ```

### Browser Launch Failures

**Problem:**
```
Error: Browser failed to launch
```

**Solutions:**
1. **Check browser installation:**
   ```bash
   playwright install firefox --force
   ```

2. **Try headless mode:**
   ```python
   automation.start_browser(headless=True)
   ```

3. **Switch browser type:**
   ```bash
   # In .env file
   BROWSER_TYPE=chromium
   ```

4. **Check system resources:**
   - Ensure sufficient RAM (4GB minimum)
   - Close other browser instances

### Email Authentication Issues

**Problem:**
```
⚠️ 未找到邮箱cookies文件
❌ 邮箱设置失败，无法继续
```

**Solutions:**
1. **Run cookie setup:**
   ```bash
   python main.py
   # Select option 3: Cookie设置
   ```

2. **Manual cookie refresh:**
   - Delete `email_cookies.json`
   - Run setup again
   - Ensure you're logged into 2925.com

3. **Check email access:**
   - Verify your 2925.com account works
   - Try logging in manually first

### Email Verification Failures

**Problem:**
```
❌ 未找到验证邮件
Exception: 邮件验证或API key获取失败
```

**Solutions:**
1. **Check email timing:**
   - Wait longer for emails (increase MAX_EMAIL_WAIT_TIME)
   - Check spam/junk folders

2. **Verify email prefix:**
   ```bash
   # Check current prefix
   grep EMAIL_PREFIX .env
   
   # Update if needed
   EMAIL_PREFIX=your_correct_prefix
   ```

3. **Manual email check:**
   - Log into 2925.com manually
   - Verify emails are arriving

### Registration Failures

**Problem:**
```
❌ 注册流程失败
Element not found or timeout
```

**Solutions:**
1. **Use intelligent mode:**
   - Always prefer intelligent automation
   - Avoid test mode for production

2. **Check network connection:**
   - Ensure stable internet
   - Try different network if possible

3. **Increase timeouts:**
   ```bash
   # In .env file
   BROWSER_TIMEOUT=60000  # 60 seconds
   WAIT_TIME_LONG=20      # 20 seconds
   ```

4. **Enable debugging:**
   ```bash
   DEBUG_MODE=true
   ENABLE_SCREENSHOTS=true
   ```

## Performance Issues

### Slow Automation

**Problem:**
Automation takes too long to complete.

**Solutions:**
1. **Use headless mode:**
   ```bash
   HEADLESS=true
   ```

2. **Optimize wait times:**
   ```bash
   WAIT_TIME_SHORT=1
   WAIT_TIME_MEDIUM=3
   WAIT_TIME_LONG=8
   ```

3. **Use faster browser:**
   ```bash
   BROWSER_TYPE=chromium
   ```

### High Resource Usage

**Problem:**
High CPU/memory usage during automation.

**Solutions:**
1. **Enable headless mode**
2. **Reduce concurrent operations**
3. **Close other applications**
4. **Use batch processing with delays**

## Configuration Issues

### Environment Variables Not Working

**Problem:**
Configuration changes in `.env` file are ignored.

**Solutions:**
1. **Check file location:**
   - `.env` should be in project root
   - Same directory as `main.py`

2. **Verify file format:**
   ```bash
   # Correct format (no spaces around =)
   EMAIL_PREFIX=myprefix
   HEADLESS=true
   
   # Incorrect format
   EMAIL_PREFIX = myprefix  # Wrong: spaces around =
   ```

3. **Restart application:**
   - Environment variables are loaded at startup
   - Restart after changes

### Invalid Configuration Values

**Problem:**
```
ValueError: invalid literal for int()
```

**Solutions:**
1. **Check numeric values:**
   ```bash
   # Correct
   WAIT_TIME_SHORT=2
   BROWSER_TIMEOUT=30000
   
   # Incorrect
   WAIT_TIME_SHORT=two  # Must be number
   ```

2. **Check boolean values:**
   ```bash
   # Correct
   HEADLESS=true
   DEBUG_MODE=false
   
   # Incorrect
   HEADLESS=yes  # Use true/false
   ```

## Network Issues

### Connection Timeouts

**Problem:**
```
TimeoutError: Waiting for element timed out
```

**Solutions:**
1. **Check internet connection**
2. **Increase timeouts:**
   ```bash
   BROWSER_TIMEOUT=60000
   MAX_EMAIL_WAIT_TIME=600
   ```

3. **Use VPN if blocked**
4. **Try different time of day**

### Rate Limiting

**Problem:**
Too many requests causing blocks.

**Solutions:**
1. **Add delays between operations:**
   ```bash
   WAIT_TIME_MEDIUM=10
   EMAIL_CHECK_INTERVAL=60
   ```

2. **Reduce batch size**
3. **Use different IP/VPN**

## Debugging Tips

### Enable Debug Mode

```bash
# In .env file
DEBUG_MODE=true
ENABLE_SCREENSHOTS=true
SAVE_HTML_LOGS=true
```

### Collect Debug Information

1. **Screenshots:** Check generated screenshots
2. **HTML Logs:** Review HTML logs in test mode
3. **Console Output:** Save console output to file
4. **Browser DevTools:** Use manual browser inspection

### Common Debug Commands

```bash
# Check installation
python -c "from src.tavily_register.main import main; print('OK')"

# Test browser launch
python -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.firefox.launch(); print('Browser OK'); b.close(); p.stop()"

# Check configuration
python -c "from src.tavily_register.config.settings import *; print(f'Prefix: {EMAIL_PREFIX}, Browser: {BROWSER_TYPE}')"
```

## Getting Help

### Log Files

Check these files for debugging information:
- `email_cookies.json` - Email authentication data
- `api_keys.md` - Successful registrations
- `test_mode_log_*.json` - HTML analysis logs (test mode)
- Screenshots with timestamps

### Reporting Issues

When reporting issues, include:
1. **Error message** (full traceback)
2. **Configuration** (sanitized .env file)
3. **System information** (OS, Python version)
4. **Steps to reproduce**
5. **Screenshots** if relevant

### Community Support

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check all documentation files
- **Examples**: Review usage examples in docs

## Prevention Tips

1. **Regular Updates:**
   - Keep dependencies updated
   - Update Playwright browsers regularly

2. **Stable Environment:**
   - Use virtual environments
   - Pin dependency versions for production

3. **Monitoring:**
   - Monitor success rates
   - Check logs regularly
   - Validate email access periodically

4. **Backup:**
   - Backup `api_keys.md` regularly
   - Save working configurations
   - Document custom settings
