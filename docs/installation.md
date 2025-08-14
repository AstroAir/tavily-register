# Installation Guide

This guide provides detailed installation instructions for the Tavily Register project.

## Prerequisites

Before installing Tavily Register, ensure you have the following:

- **Python 3.12+**: The project requires Python 3.12 or higher
- **Network Connection**: Required for downloading dependencies and accessing Tavily/email services
- **2925.com Email Account**: You'll need access to a 2925.com email account for verification

## Installation Methods

### Method 1: Automatic Installation (Recommended)

The easiest way to install Tavily Register is using the automated setup script:

```bash
# Clone the repository
git clone https://github.com/yatotm/tavily-register.git
cd tavily-register

# Run automatic installation
python scripts/setup.py
```

The setup script will:
- Check Python version compatibility
- Install all required dependencies
- Install Playwright browsers
- Create environment configuration files
- Run basic tests to verify installation

### Method 2: Manual Installation

For more control over the installation process:

```bash
# Clone the repository
git clone https://github.com/yatotm/tavily-register.git
cd tavily-register

# Install the package and dependencies
pip install -e .

# Install Playwright browsers
playwright install firefox

# Optional: Install development dependencies
pip install -e ".[dev]"
```

### Method 3: Development Installation

For developers who want to contribute to the project:

```bash
# Clone the repository
git clone https://github.com/yatotm/tavily-register.git
cd tavily-register

# Install in development mode with all dependencies
pip install -e ".[dev,test]"

# Install Playwright browsers
playwright install

# Install pre-commit hooks (optional)
pre-commit install
```

## Configuration

### Environment Configuration

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file with your settings:**
   ```bash
   # Required: Set your email prefix
   EMAIL_PREFIX=your_prefix

   # Optional: Customize other settings
   BROWSER_TYPE=firefox
   HEADLESS=false
   ```

### Email Setup

1. **Configure your email prefix** in the `.env` file or `src/tavily_register/config/settings.py`
2. **Run the initial setup** to configure email cookies:
   ```bash
   python main.py
   ```
3. **Follow the prompts** to log into your 2925.com email account

## Verification

To verify your installation is working correctly:

```bash
# Run the basic test
python scripts/setup.py

# Or test manually
python -c "from src.tavily_register.main import main; print('Installation successful!')"
```

## Troubleshooting

### Common Issues

**Python Version Error:**
```
Error: Python version too low
```
- Solution: Upgrade to Python 3.12 or higher

**Playwright Installation Failed:**
```
Error: Failed to install Playwright browsers
```
- Solution: Run `playwright install firefox` manually
- Alternative: Try `playwright install chromium` if Firefox fails

**Import Errors:**
```
ModuleNotFoundError: No module named 'src.tavily_register'
```
- Solution: Ensure you installed with `pip install -e .`
- Alternative: Run from the project root directory

**Permission Errors:**
```
PermissionError: [Errno 13] Permission denied
```
- Solution: Use `pip install --user -e .` for user-level installation
- Alternative: Use a virtual environment

### Virtual Environment Setup

For isolated installation:

```bash
# Create virtual environment
python -m venv tavily-env

# Activate (Windows)
tavily-env\Scripts\activate

# Activate (Linux/Mac)
source tavily-env/bin/activate

# Install
pip install -e .
```

## Next Steps

After successful installation:

1. **Read the [Usage Guide](usage.md)** for detailed usage instructions
2. **Configure your email settings** as described above
3. **Run your first automation** with `python main.py`
4. **Check the [Troubleshooting Guide](troubleshooting.md)** if you encounter issues

## System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: At least 1GB free space
- **Network**: Stable internet connection for web automation
