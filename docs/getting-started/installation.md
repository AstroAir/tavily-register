# Installation Guide

This comprehensive guide will walk you through installing Tavily Register on your system.

## System Requirements

!!! info "Minimum Requirements"
    - **Python**: 3.12 or higher
    - **Operating System**: Windows 10+, macOS 10.14+, or Linux
    - **Memory**: 4GB RAM (8GB recommended)
    - **Storage**: 1GB free space
    - **Network**: Stable internet connection

!!! tip "Recommended Setup"
    - Use a virtual environment for Python dependencies
    - Install on SSD for better performance
    - Ensure antivirus software doesn't block browser automation

## Installation Methods

=== "Automatic Installation"

    **Recommended for most users**

    ```bash
    # Clone the repository
    git clone https://github.com/yatotm/tavily-register.git
    cd tavily-register
    
    # Run automatic installation
    python scripts/setup.py
    ```

    The setup script will:
    
    - ✅ Check Python version compatibility
    - ✅ Install all required dependencies
    - ✅ Install Playwright browsers
    - ✅ Create environment configuration files
    - ✅ Run basic tests to verify installation

=== "Manual Installation"

    **For users who want more control**

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

=== "Development Installation"

    **For contributors and developers**

    ```bash
    # Clone the repository
    git clone https://github.com/yatotm/tavily-register.git
    cd tavily-register
    
    # Install in development mode with all dependencies
    pip install -e ".[dev,test,docs]"
    
    # Install all Playwright browsers
    playwright install
    
    # Install pre-commit hooks
    pre-commit install
    
    # Verify installation
    pytest tests/
    ```

=== "Docker Installation"

    **For containerized deployment**

    ```bash
    # Clone the repository
    git clone https://github.com/yatotm/tavily-register.git
    cd tavily-register
    
    # Build Docker image
    docker build -t tavily-register .
    
    # Run container
    docker run -it --rm tavily-register
    ```

## Virtual Environment Setup

!!! warning "Highly Recommended"
    Always use a virtual environment to avoid dependency conflicts.

=== "venv (Built-in)"

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

=== "conda"

    ```bash
    # Create conda environment
    conda create -n tavily-register python=3.12
    
    # Activate environment
    conda activate tavily-register
    
    # Install
    pip install -e .
    ```

=== "poetry"

    ```bash
    # Install poetry if not already installed
    pip install poetry
    
    # Install dependencies
    poetry install
    
    # Activate shell
    poetry shell
    ```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required: Set your email prefix
EMAIL_PREFIX=your_prefix

# Optional: Browser configuration
BROWSER_TYPE=firefox
HEADLESS=false

# Optional: Timing configuration
WAIT_TIME_SHORT=2
WAIT_TIME_MEDIUM=5
WAIT_TIME_LONG=10

# Optional: Debug settings
DEBUG=false
LOG_LEVEL=INFO
```

### Email Configuration

1. **Set your email prefix** in the `.env` file
2. **Run initial setup** to configure email cookies:
   ```bash
   python main.py
   ```
3. **Follow the prompts** to log into your 2925.com email account

## Verification

### Quick Test

```bash
# Test installation
python -c "from src.tavily_register.main import main; print('✅ Installation successful!')"
```

### Full Test Suite

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src/tavily_register tests/

# Run specific test categories
pytest -m "not slow" tests/  # Skip slow tests
pytest -m integration tests/  # Run integration tests only
```

### Browser Test

```bash
# Test browser installation
playwright install --dry-run firefox
```

## Troubleshooting

### Common Issues

??? failure "Python Version Error"
    ```
    Error: Python version too low
    ```
    
    **Solution:**
    
    1. Check your Python version: `python --version`
    2. Install Python 3.12+ from [python.org](https://python.org)
    3. Use `python3.12` explicitly if multiple versions are installed

??? failure "Playwright Installation Failed"
    ```
    Error: Failed to install Playwright browsers
    ```
    
    **Solutions:**
    
    1. Run manually: `playwright install firefox`
    2. Try alternative browser: `playwright install chromium`
    3. Check network connection and firewall settings
    4. Use system package manager on Linux:
       ```bash
       # Ubuntu/Debian
       sudo apt-get install firefox
       
       # CentOS/RHEL
       sudo yum install firefox
       ```

??? failure "Import Errors"
    ```
    ModuleNotFoundError: No module named 'src.tavily_register'
    ```
    
    **Solutions:**
    
    1. Ensure you installed with: `pip install -e .`
    2. Run from the project root directory
    3. Check virtual environment is activated
    4. Verify PYTHONPATH includes the project directory

??? failure "Permission Errors"
    ```
    PermissionError: [Errno 13] Permission denied
    ```
    
    **Solutions:**
    
    1. Use user-level installation: `pip install --user -e .`
    2. Use virtual environment (recommended)
    3. On Linux/Mac, avoid using `sudo` with pip
    4. Check file permissions: `chmod +x scripts/setup.py`

### Platform-Specific Issues

=== "Windows"

    **PowerShell Execution Policy:**
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
    
    **Long Path Support:**
    Enable long path support in Windows settings or registry.

=== "macOS"

    **Xcode Command Line Tools:**
    ```bash
    xcode-select --install
    ```
    
    **Homebrew Dependencies:**
    ```bash
    brew install python@3.12
    ```

=== "Linux"

    **System Dependencies:**
    ```bash
    # Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install python3.12 python3.12-venv python3.12-dev
    
    # CentOS/RHEL
    sudo yum install python312 python312-devel
    
    # Arch Linux
    sudo pacman -S python
    ```

## Next Steps

After successful installation:

1. **[Quick Start Guide](quick-start.md)** - Get running in minutes
2. **[Configuration Guide](configuration.md)** - Customize your setup
3. **[User Guide](../user-guide/index.md)** - Learn all features
4. **[Troubleshooting](../troubleshooting/index.md)** - Solve common issues

## Getting Help

If you're still having trouble:

- 📖 Check the [Troubleshooting Guide](../troubleshooting/index.md)
- 🐛 [Report a bug](https://github.com/yatotm/tavily-register/issues/new?template=bug_report.md)
- 💬 [Ask a question](https://github.com/yatotm/tavily-register/discussions)
- 📧 Email: support@tavily-register.com
