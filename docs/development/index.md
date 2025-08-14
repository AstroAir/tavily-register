# Development Guide

Welcome to the Tavily Register development guide! This section provides comprehensive information for contributors, developers, and maintainers working on the project.

## Development Overview

Tavily Register is built with modern Python practices and follows industry standards for code quality, testing, and documentation.

<div class="grid cards" markdown>

-   :material-heart:{ .lg .middle } **Contributing**

    ---

    Guidelines for contributing to the project

    [:octicons-arrow-right-24: Contributing Guide](contributing.md)

-   :material-test-tube:{ .lg .middle } **Testing**

    ---

    Testing strategies and test execution

    [:octicons-arrow-right-24: Testing Guide](testing.md)

-   :material-rocket-launch:{ .lg .middle } **Release Process**

    ---

    How releases are created and deployed

    [:octicons-arrow-right-24: Release Process](release-process.md)

</div>

## Quick Development Setup

### Prerequisites

- **Python 3.12+**
- **Git**
- **Node.js 18+** (for documentation)
- **Docker** (optional, for containerized development)

### Setup Development Environment

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/tavily-register.git
cd tavily-register

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install development dependencies
pip install -e ".[dev,test,docs]"

# 4. Install pre-commit hooks
pre-commit install

# 5. Install Playwright browsers
playwright install

# 6. Run tests to verify setup
pytest tests/
```

### Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make changes and test
pytest tests/
black src/ tests/
flake8 src/ tests/
mypy src/

# 3. Run documentation build
mkdocs build

# 4. Commit changes
git add .
git commit -m "feat: add your feature description"

# 5. Push and create PR
git push origin feature/your-feature-name
```

## Project Structure

```
tavily-register/
├── .github/                    # GitHub workflows and templates
│   ├── workflows/             # CI/CD workflows
│   └── ISSUE_TEMPLATE/        # Issue templates
├── docs/                      # Documentation source
│   ├── getting-started/       # Getting started guides
│   ├── user-guide/           # User documentation
│   ├── api/                  # API reference
│   ├── examples/             # Code examples
│   ├── troubleshooting/      # Troubleshooting guides
│   ├── development/          # Development guides
│   └── assets/               # Documentation assets
├── src/                      # Source code
│   └── tavily_register/      # Main package
│       ├── core/             # Core automation modules
│       ├── email/            # Email handling
│       ├── config/           # Configuration
│       └── utils/            # Utility functions
├── tests/                    # Test files
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── fixtures/             # Test fixtures
├── scripts/                  # Utility scripts
├── examples/                 # Usage examples
├── mkdocs.yml               # Documentation configuration
├── pyproject.toml           # Project configuration
└── README.md                # Project README
```

## Code Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

```python
# Line length: 88 characters (Black default)
# Use type hints for all functions
def process_data(input_data: List[str]) -> Dict[str, Any]:
    """Process input data and return results.
    
    Args:
        input_data: List of strings to process
        
    Returns:
        Dictionary containing processed results
        
    Raises:
        ValueError: If input_data is empty
    """
    if not input_data:
        raise ValueError("Input data cannot be empty")
    
    return {"processed": len(input_data)}
```

### Code Quality Tools

We use these tools to maintain code quality:

```bash
# Code formatting
black src/ tests/ scripts/

# Import sorting
isort src/ tests/ scripts/

# Linting
flake8 src/ tests/ scripts/

# Type checking
mypy src/

# Security scanning
bandit -r src/

# Dependency checking
safety check
```

### Pre-commit Hooks

Pre-commit hooks automatically run quality checks:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
        language_version: python3.12

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.6.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

## Testing Strategy

### Test Categories

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete workflows
4. **Performance Tests**: Test performance characteristics

### Running Tests

```bash
# Run all tests
pytest

# Run specific test categories
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests only
pytest -m "not slow"     # Skip slow tests

# Run with coverage
pytest --cov=src/tavily_register --cov-report=html

# Run performance tests
pytest -m performance --benchmark-only
```

### Writing Tests

```python
import pytest
from unittest.mock import Mock, patch
from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation

class TestIntelligentAutomation:
    """Test cases for intelligent automation."""
    
    def test_initialization(self):
        """Test automation initialization."""
        automation = IntelligentTavilyAutomation()
        assert automation is not None
        assert hasattr(automation, 'email_prefix')
    
    @pytest.mark.integration
    def test_browser_startup(self):
        """Test browser startup integration."""
        automation = IntelligentTavilyAutomation()
        try:
            automation.start_browser(headless=True)
            assert automation.browser is not None
        finally:
            automation.close_browser()
    
    @patch('src.tavily_register.core.intelligent_automation.sync_playwright')
    def test_mocked_automation(self, mock_playwright):
        """Test with mocked dependencies."""
        mock_browser = Mock()
        mock_playwright.return_value.__enter__.return_value.firefox.launch.return_value = mock_browser
        
        automation = IntelligentTavilyAutomation()
        automation.start_browser()
        
        mock_playwright.return_value.__enter__.return_value.firefox.launch.assert_called_once()
```

## Documentation Development

### Local Documentation Server

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Start development server
python scripts/setup_docs.py serve

# Or use MkDocs directly
mkdocs serve

# Build static documentation
mkdocs build
```

### Documentation Standards

1. **Use clear, concise language**
2. **Include code examples** for all features
3. **Add screenshots** for UI-related content
4. **Use admonitions** for important information
5. **Keep content up-to-date** with code changes

### Writing Documentation

```markdown
# Page Title

Brief introduction to the topic.

## Section Title

Content with examples:

```python
# Code example
from src.tavily_register import example_function

result = example_function("parameter")
print(result)
```

!!! tip "Pro Tip"
    Use admonitions to highlight important information.

!!! warning "Important"
    Critical information that users must know.
```

## API Design Principles

### Class Design

```python
class AutomationBase:
    """Base class for automation implementations.
    
    This class provides common functionality for all automation types.
    """
    
    def __init__(self, email_prefix: Optional[str] = None) -> None:
        """Initialize automation instance.
        
        Args:
            email_prefix: Custom email prefix for generated emails
        """
        self.email_prefix = email_prefix or self._get_default_prefix()
        self._browser: Optional[Browser] = None
    
    def start_browser(self, headless: bool = False) -> None:
        """Start browser instance.
        
        Args:
            headless: Whether to run in headless mode
            
        Raises:
            BrowserError: If browser fails to start
        """
        try:
            # Implementation
            pass
        except Exception as e:
            raise BrowserError(f"Failed to start browser: {e}") from e
    
    def close_browser(self) -> None:
        """Close browser and cleanup resources."""
        if self._browser:
            self._browser.close()
            self._browser = None
```

### Error Handling

```python
# Custom exceptions
class TavilyRegisterError(Exception):
    """Base exception for Tavily Register."""
    pass

class BrowserError(TavilyRegisterError):
    """Browser-related errors."""
    pass

class EmailError(TavilyRegisterError):
    """Email-related errors."""
    pass

class ConfigurationError(TavilyRegisterError):
    """Configuration-related errors."""
    pass

# Usage in code
def risky_operation():
    try:
        # Risky code
        pass
    except SpecificError as e:
        logger.error(f"Specific error occurred: {e}")
        raise EmailError(f"Email operation failed: {e}") from e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise TavilyRegisterError(f"Operation failed: {e}") from e
```

## Performance Guidelines

### Memory Management

```python
# Use context managers for resource cleanup
from contextlib import contextmanager

@contextmanager
def automation_context(email_prefix: str):
    """Context manager for automation instances."""
    automation = IntelligentTavilyAutomation(email_prefix=email_prefix)
    try:
        automation.start_browser()
        yield automation
    finally:
        automation.close_browser()

# Usage
with automation_context("test_prefix") as automation:
    result = automation.run_automation()
```

### Async Patterns

```python
import asyncio
from playwright.async_api import async_playwright

async def async_automation(email_prefix: str) -> bool:
    """Async automation implementation."""
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        try:
            # Async automation logic
            return True
        finally:
            await browser.close()

# Concurrent execution
async def run_multiple_automations(prefixes: List[str]) -> List[bool]:
    """Run multiple automations concurrently."""
    tasks = [async_automation(prefix) for prefix in prefixes]
    return await asyncio.gather(*tasks)
```

## Security Considerations

### Sensitive Data Handling

```python
import os
from typing import Optional

def get_sensitive_config(key: str) -> Optional[str]:
    """Get sensitive configuration from environment."""
    value = os.getenv(key)
    if value:
        # Don't log sensitive values
        logger.info(f"Loaded configuration for {key}")
    else:
        logger.warning(f"Configuration {key} not found")
    return value

# Usage
email_prefix = get_sensitive_config("EMAIL_PREFIX")
```

### Input Validation

```python
import re
from typing import Union

def validate_email_prefix(prefix: str) -> str:
    """Validate email prefix format.
    
    Args:
        prefix: Email prefix to validate
        
    Returns:
        Validated prefix
        
    Raises:
        ValueError: If prefix is invalid
    """
    if not prefix:
        raise ValueError("Email prefix cannot be empty")
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', prefix):
        raise ValueError("Email prefix contains invalid characters")
    
    if len(prefix) > 50:
        raise ValueError("Email prefix too long")
    
    return prefix.lower()
```

## Debugging and Profiling

### Debug Configuration

```python
import logging
import sys

def setup_debug_logging():
    """Setup debug logging configuration."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('debug.log')
        ]
    )

# Performance profiling
import cProfile
import pstats

def profile_automation():
    """Profile automation performance."""
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run automation
    automation = IntelligentTavilyAutomation()
    automation.run_automation()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)
```

## Continuous Integration

Our CI/CD pipeline includes:

1. **Code Quality Checks**: Linting, formatting, type checking
2. **Security Scanning**: Dependency vulnerabilities, code security
3. **Testing**: Unit, integration, and performance tests
4. **Documentation**: Build and deploy documentation
5. **Release**: Automated versioning and publishing

### GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: pip install -e ".[dev,test]"
      
      - name: Code quality checks
        run: |
          black --check src/ tests/
          flake8 src/ tests/
          mypy src/
          bandit -r src/
  
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev,test]"
          playwright install firefox
      
      - name: Run tests
        run: pytest --cov=src/tavily_register --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Getting Help

For development questions:

- 📖 [Contributing Guide](contributing.md) - Detailed contribution instructions
- 🧪 [Testing Guide](testing.md) - Testing best practices
- 🚀 [Release Process](release-process.md) - How releases work
- 💬 [Discussions](https://github.com/yatotm/tavily-register/discussions) - Community Q&A
- 📧 [Maintainer Email](mailto:maintainers@tavily-register.com) - Direct contact
