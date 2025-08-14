# Usage Guide

This guide provides comprehensive instructions for using Tavily Register to automate API key registration.

## Quick Start

### Basic Usage

1. **Start the application:**
   ```bash
   python main.py
   ```

2. **Choose your operation mode:**
   - **Intelligent Automation Mode** (Recommended): Advanced automation with 95%+ success rate
   - **Test Mode**: Traditional approach for debugging and analysis
   - **Cookie Setup**: Configure email authentication

3. **Configure settings** when prompted:
   - Browser mode (foreground/background)
   - Number of accounts to register (1-10)

### First-Time Setup

Before running automation, you need to set up email authentication:

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Select option 3 (Cookie Setup)**

3. **Follow the browser prompts** to log into your 2925.com email account

4. **Confirm the setup** - the system will automatically extract your email prefix

## Operation Modes

### Intelligent Automation Mode

The recommended mode that uses advanced HTML analysis and smart waiting mechanisms:

**Features:**
- 60-70% performance improvement over traditional methods
- 95%+ success rate
- Intelligent element detection
- Dynamic waiting mechanisms
- Automatic error recovery

**Usage:**
```bash
python main.py
# Select option 1: Intelligent Automation Mode
# Configure browser mode and account count
# Confirm to start automation
```

**Process Flow:**
1. **Registration Phase**: Automatically fills Tavily registration form
2. **Email Verification**: Monitors email for verification messages
3. **Login Phase**: Automatically logs into Tavily account
4. **API Acquisition**: Extracts API key from dashboard
5. **Data Storage**: Saves account information to `api_keys.md`

### Test Mode

Traditional automation approach with HTML information collection:

**Features:**
- Traditional waiting + keyword-based detection
- HTML information logging for optimization
- Debugging capabilities
- Performance comparison baseline

**Usage:**
```bash
python main.py
# Select option 2: Test Mode
# Configure settings as needed
# Review HTML logs for analysis
```

## Configuration Options

### Environment Variables

Configure the application using `.env` file:

```bash
# Email Configuration
EMAIL_PREFIX=your_prefix
EMAIL_DOMAIN=2925.com

# Browser Settings
BROWSER_TYPE=firefox          # Options: firefox, chromium, webkit
HEADLESS=false               # true for background mode
BROWSER_TIMEOUT=30000        # 30 seconds

# Wait Times (seconds)
WAIT_TIME_SHORT=2
WAIT_TIME_MEDIUM=5
WAIT_TIME_LONG=10
EMAIL_CHECK_INTERVAL=30
MAX_EMAIL_WAIT_TIME=300      # 5 minutes

# File Paths
API_KEYS_FILE=api_keys.md
COOKIES_FILE=email_cookies.json

# Development
DEBUG_MODE=false
ENABLE_SCREENSHOTS=true
SAVE_HTML_LOGS=true
```

### Runtime Configuration

During execution, you can configure:

- **Browser Mode**: Foreground (visible) or background (headless)
- **Account Count**: Number of accounts to register (1-10)
- **Email Prefix**: Automatically detected from cookies or manually set

## Output Format

### API Keys File

Registered accounts are saved to `api_keys.md`:

```text
user123-abc123@2925.com,TavilyAuto123!,tvly-dev-xxxxxxxxxx,2025-01-01 12:00:00;
user123-def456@2925.com,TavilyAuto123!,tvly-dev-yyyyyyyyyy,2025-01-01 12:05:00;
```

**Format:** `Email,Password,API_Key,Registration_Time`

### Console Output

The application provides detailed console output:

```
🚀 智能Tavily自动注册系统
====================================
🌟 基于深层HTML分析的智能自动化解决方案
⚡ 性能提升60-70% | 成功率95%+ | 完全自动化
📧 当前邮箱前缀: user123

🎛️ 选择运行模式:
1. 智能自动化模式 (推荐)
2. 测试模式 (传统方式+HTML信息收集)
3. Cookie设置
4. 退出
```

## Advanced Usage

### Batch Registration

Register multiple accounts in sequence:

```python
# Configure for batch processing
count = 5  # Register 5 accounts
headless = True  # Use background mode for faster processing

# The system will automatically:
# 1. Generate unique email addresses
# 2. Register each account
# 3. Verify emails
# 4. Extract API keys
# 5. Save all information
```

### Custom Email Prefixes

Use different email prefixes for organization:

```bash
# Method 1: Environment variable
export EMAIL_PREFIX=project_alpha

# Method 2: .env file
echo "EMAIL_PREFIX=project_alpha" >> .env

# Method 3: Direct configuration
# Edit src/tavily_register/config/settings.py
```

### Browser Selection

Choose different browsers based on your needs:

```bash
# Firefox (default, most stable)
BROWSER_TYPE=firefox

# Chromium (faster, good compatibility)
BROWSER_TYPE=chromium

# WebKit (Safari engine, for testing)
BROWSER_TYPE=webkit
```

## Best Practices

### Performance Optimization

1. **Use Intelligent Mode**: Always prefer intelligent automation over test mode
2. **Background Mode**: Use headless mode for better performance
3. **Batch Processing**: Register multiple accounts in one session
4. **Stable Network**: Ensure reliable internet connection

### Error Handling

1. **Monitor Console Output**: Watch for error messages and warnings
2. **Check Email Access**: Ensure your 2925.com account is accessible
3. **Verify Cookies**: Refresh email cookies if authentication fails
4. **Review Logs**: Check HTML logs in test mode for debugging

### Security Considerations

1. **Protect Credentials**: Keep your `.env` file secure
2. **API Key Storage**: Secure the `api_keys.md` file
3. **Cookie Management**: Regularly refresh email cookies
4. **Network Security**: Use secure networks for automation

## Troubleshooting

For common issues and solutions, see the [Troubleshooting Guide](troubleshooting.md).

## Examples

### Example 1: Single Account Registration

```bash
python main.py
# Select: 1 (Intelligent Mode)
# Browser: 1 (Foreground)
# Count: 1
# Confirm: y
```

### Example 2: Batch Registration

```bash
python main.py
# Select: 1 (Intelligent Mode)
# Browser: 2 (Background)
# Count: 5
# Confirm: y
```

### Example 3: Debug Mode

```bash
python main.py
# Select: 2 (Test Mode)
# Browser: 1 (Foreground)
# Count: 1
# Review HTML logs after completion
```
