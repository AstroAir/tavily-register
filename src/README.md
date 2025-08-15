# Source Code Directory

This directory contains the main source code for the Tavily Register application.

## Structure

- **tavily_register/**: Main application package
  - **core/**: Core automation modules
  - **email/**: Email handling functionality  
  - **config/**: Configuration management
  - **utils/**: Utility functions and helpers

## Package Organization

The source code follows Python package best practices with proper module separation and clear import hierarchies.

### Core Modules

- `intelligent_automation.py`: Advanced automation using intelligent element detection
- `traditional_automation.py`: Traditional automation approach for testing and comparison

### Email Modules

- `checker.py`: Email verification and checking functionality
- `login_helper.py`: Email login assistance and enhanced cookie management

### Configuration

- `settings.py`: All application configuration constants and settings with .env file support

### Utilities

- `helpers.py`: Common utility functions with enhanced cookie handling

## Recent Improvements

### Enhanced Cookie Management
- **Fixed Cookie Logic**: Corrected the cookie saving flow in main.py to properly save cookies after user login
- **Enhanced Persistence**: Added cookie expiry validation (7-day limit) and better error handling
- **Improved Format Handling**: Added cookie format validation and Playwright compatibility functions
- **Metadata Tracking**: Cookies now saved with timestamps and count information for better tracking

### Environment Variable Support
- **Added .env File Loading**: Implemented python-dotenv integration for loading configuration from .env files
- **Flexible Configuration**: Supports both direct environment variables and .env file configuration
- **Auto-detection**: Automatically finds and loads .env files from project root or current directory
- **Graceful Fallback**: Falls back to default values if .env file is not found or python-dotenv is not installed

## Development Guidelines

When working with the source code:

1. **Follow PEP 8** style guidelines
2. **Use type hints** for function parameters and return values
3. **Write comprehensive docstrings** for all public functions and classes
4. **Use relative imports** for internal modules
5. **Add tests** for new functionality
6. **Update documentation** when making changes

## Import Structure

The package uses relative imports for internal modules:

```python
# Correct internal imports
from .config.settings import EMAIL_DOMAIN, BROWSER_TYPE
from .utils.helpers import generate_email, save_api_key
from .core.intelligent_automation import IntelligentTavilyAutomation

# External imports
from playwright.sync_api import sync_playwright
import time
import json
```

## Testing

Tests for the source code are located in the `tests/` directory at the project root. Run tests using:

```bash
pytest tests/
```

## Module Details

### Main Controller (`main.py`)

The `TavilyMainController` class provides the interactive interface and orchestrates the automation workflow. It handles user input, configuration management, and coordinates between different automation modes.

### Core Automation (`core/`)

- **Intelligent Mode**: Uses advanced HTML analysis and smart waiting mechanisms for optimal performance
- **Traditional Mode**: Provides baseline functionality and HTML logging for debugging and optimization

### Email Integration (`email/`)

- **Checker**: Monitors 2925.com email service for verification messages
- **Login Helper**: Manages email authentication and cookie persistence

### Configuration (`config/`)

- **Environment Support**: Reads from environment variables and .env files
- **Type Safety**: Provides type conversion and validation for configuration values
- **Centralized Settings**: Single source of truth for all application configuration
