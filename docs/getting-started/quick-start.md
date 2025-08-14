# Quick Start Guide

Get up and running with Tavily Register in just a few minutes! This guide will walk you through the essential steps to start automating your Tavily API key registration.

## 🚀 5-Minute Setup

### Step 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/yatotm/tavily-register.git
cd tavily-register

# Quick install with automatic setup
python scripts/setup.py
```

!!! tip "Alternative Installation"
    If the automatic setup doesn't work, try the [manual installation](installation.md#manual-installation) method.

### Step 2: Configure Email

Edit your email settings:

=== "Environment File"

    Create a `.env` file:
    ```bash
    # Required: Your 2925.com email prefix
    EMAIL_PREFIX=your_prefix_here
    
    # Optional: Browser settings
    BROWSER_TYPE=firefox
    HEADLESS=false
    ```

=== "Settings File"

    Edit `src/tavily_register/config/settings.py`:
    ```python
    # Replace with your actual email prefix
    EMAIL_PREFIX = "your_prefix_here"
    ```

### Step 3: Setup Email Authentication

```bash
# Run the application
python main.py

# Choose option 3: "设置邮箱登录Cookie"
# Follow the prompts to log into your 2925.com email
```

### Step 4: Run Your First Automation

```bash
# Run the application again
python main.py

# Choose option 1: "智能自动化模式 (推荐)"
# Sit back and watch the magic happen! ✨
```

## 🎯 What Happens Next?

The automation will:

1. **Generate a unique email** using your prefix
2. **Navigate to Tavily** registration page
3. **Fill out the form** automatically
4. **Verify the email** by checking your inbox
5. **Complete registration** and login
6. **Extract the API key** and save it

## 📋 Expected Output

After successful completion, you'll find your API key in `api_keys.md`:

```text
your_prefix-abc123@2925.com,TavilyAuto123!,tvly-dev-xxxxxxxxxx,2025-01-01 12:00:00;
```

## 🔧 Quick Configuration Options

### Browser Settings

=== "Firefox (Recommended)"

    ```python
    BROWSER_TYPE = "firefox"
    HEADLESS = False  # Set to True for background operation
    ```

=== "Chromium"

    ```python
    BROWSER_TYPE = "chromium"
    HEADLESS = False
    ```

### Timing Settings

```python
# Adjust wait times if needed
WAIT_TIME_SHORT = 2    # Quick operations
WAIT_TIME_MEDIUM = 5   # Form filling
WAIT_TIME_LONG = 10    # Email verification
```

## 🎮 Operation Modes

### Intelligent Mode (Recommended)

- **Best Performance**: 95%+ success rate
- **Smart Detection**: Advanced element recognition
- **Optimized Speed**: 60-70% faster than traditional methods

```bash
python main.py
# Choose option 1
```

### Test Mode

- **Debugging**: Detailed HTML logging
- **Analysis**: Performance comparison
- **Troubleshooting**: Step-by-step execution

```bash
python main.py
# Choose option 2
```

## ⚡ Pro Tips

!!! tip "Performance Optimization"
    - Use **Firefox** for best compatibility
    - Keep **HEADLESS=False** during initial setup
    - Ensure stable internet connection
    - Close unnecessary browser windows

!!! warning "Email Requirements"
    - Must have a valid **2925.com** email account
    - Email prefix should be **unique** and **memorable**
    - Avoid special characters in the prefix

!!! info "Troubleshooting"
    - Check the [Common Issues](../troubleshooting/common-issues.md) if something goes wrong
    - Enable debug mode by setting `DEBUG=True` in your `.env` file
    - Screenshots are automatically saved for failed attempts

## 🔄 Running Multiple Registrations

To register multiple API keys:

```bash
# Run the application multiple times
python main.py

# Or use the batch script (if available)
python scripts/batch_register.py --count 5
```

Each run will generate a new unique email and API key.

## 📊 Monitoring Progress

Watch for these indicators:

- ✅ **Green messages**: Successful operations
- ⚠️ **Yellow messages**: Warnings or retries
- ❌ **Red messages**: Errors requiring attention
- 📧 **Email icons**: Email-related operations
- 🔑 **Key icons**: API key extraction

## 🆘 Quick Troubleshooting

### Common Issues

??? failure "Browser Not Found"
    ```bash
    # Install browser manually
    playwright install firefox
    ```

??? failure "Email Login Failed"
    ```bash
    # Clear cookies and try again
    rm email_cookies.json
    python main.py  # Choose option 3
    ```

??? failure "Registration Failed"
    ```bash
    # Try test mode for debugging
    python main.py  # Choose option 2
    ```

### Getting Help

- 📖 [Full Troubleshooting Guide](../troubleshooting/index.md)
- 🐛 [Report Issues](https://github.com/yatotm/tavily-register/issues)
- 💬 [Community Discussions](https://github.com/yatotm/tavily-register/discussions)

## 🎉 Success!

Congratulations! You've successfully set up Tavily Register. Your API key is now ready to use for your projects.

## 📚 Next Steps

<div class="grid cards" markdown>

-   :material-book-open-page-variant:{ .lg .middle } **Learn More**

    ---

    Explore advanced features and configuration options

    [:octicons-arrow-right-24: User Guide](../user-guide/index.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Detailed documentation of all classes and methods

    [:octicons-arrow-right-24: API Docs](../api/index.md)

-   :material-code-braces:{ .lg .middle } **Examples**

    ---

    Practical examples and use cases

    [:octicons-arrow-right-24: Examples](../examples/index.md)

-   :material-hammer-wrench:{ .lg .middle } **Contribute**

    ---

    Help improve the project

    [:octicons-arrow-right-24: Contributing](../development/contributing.md)

</div>

---

**Happy automating!** 🤖✨
