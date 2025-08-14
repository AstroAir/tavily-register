# Tavily Register

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[English](README_EN.md) | 中文

An intelligent automation solution for Tavily API key registration based on deep HTML analysis, providing end-to-end automated API key acquisition.

## ✨ Features

- 🧠 **Intelligent Automation**: Advanced element detection and smart waiting mechanisms
- 🚀 **High Performance**: 60-70% performance improvement with 95%+ success rate
- 📧 **Email Integration**: Automated email verification and cookie management
- 🔧 **Flexible Configuration**: Support for multiple browser types and modes
- 🛡️ **Error Handling**: Robust error handling and recovery mechanisms
- 📊 **Detailed Logging**: Comprehensive logging and HTML information collection

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Network connection
- 2925.com email account

### Installation

```bash
# Clone the repository
git clone https://github.com/yatotm/tavily-register.git
cd tavily-register

# Automatic installation
python scripts/setup.py

# Or manual installation
pip install -e .
playwright install firefox
```

### Configuration

1. **Set Email Prefix**

   Edit `src/tavily_register/config/settings.py`:
   ```python
   EMAIL_PREFIX = "your_prefix"  # Replace with your 2925.com email prefix
   ```

2. **Set Up Email Login**
   ```bash
   python main.py
   ```
   Follow the prompts to complete 2925.com email login and save cookies.

### Usage

```bash
python main.py
```

Choose operation mode:
- **Intelligent Automation Mode** (Recommended): Efficient and stable automation process
- **Test Mode**: Traditional approach for debugging and HTML information collection

## 📁 Project Structure

```
tavily-register/
├── .github/                          # GitHub specific files
│   ├── workflows/                    # CI/CD workflows
│   └── ISSUE_TEMPLATE/              # Issue templates
├── docs/                            # Documentation
├── src/                             # Source code
│   └── tavily_register/             # Main package
│       ├── core/                    # Core automation modules
│       ├── email/                   # Email handling
│       ├── config/                  # Configuration
│       └── utils/                   # Utility functions
├── tests/                           # Test files
├── scripts/                         # Utility scripts
├── examples/                        # Usage examples
├── main.py                          # Main entry point
├── requirements.txt                 # Dependencies
└── pyproject.toml                   # Project configuration
```

## 🔄 Workflow

1. **Registration Phase**: Automatically fill out Tavily registration form
2. **Email Verification**: Intelligently detect verification emails and click verification links
3. **Login Phase**: Automatically log into Tavily account
4. **API Acquisition**: Intelligently identify and obtain API Key
5. **Data Storage**: Save account information and API Key to file

## 📤 Output Format

API Keys are saved in `api_keys.md` file:

```text
user123-abc123@2925.com,TavilyAuto123!,tvly-dev-xxxxxxxxxx,2025-01-01 12:00:00;
```

Format: `Email,Password,API_Key,Time`

## 🛠️ Configuration

### Browser Configuration

```python
HEADLESS = False          # Whether to run in headless mode
BROWSER_TYPE = "firefox"  # Browser type
```

### Wait Time Configuration

```python
WAIT_TIME_SHORT = 2       # Short wait time
WAIT_TIME_MEDIUM = 5      # Medium wait time
WAIT_TIME_LONG = 10       # Long wait time
```

### Email Configuration

```python
EMAIL_DOMAIN = "2925.com"
EMAIL_PREFIX = "user123"  # Your email prefix
```

## 🧪 Testing

Run tests to ensure everything works correctly:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/tavily_register

# Run specific test
pytest tests/unit/test_automation.py
```

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [Usage Examples](docs/usage.md)
- [API Reference](docs/api.md)
- [Troubleshooting](docs/troubleshooting.md)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📋 Tech Stack

- **Python 3.12+**
- **Playwright**: Web automation
- **BeautifulSoup4**: HTML parsing
- **pytest**: Testing framework

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Please comply with the terms of service of relevant websites when using.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
