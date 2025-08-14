# Contributing to Tavily Register

Thank you for your interest in contributing to Tavily Register! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Git
- Basic understanding of web automation and Playwright

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/tavily-register.git
   cd tavily-register
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   playwright install firefox
   ```

4. **Run Tests**
   ```bash
   pytest
   ```

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use Black for code formatting: `black src/ tests/`
- Use isort for import sorting: `isort src/ tests/`
- Maximum line length: 88 characters

### Commit Messages

Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test additions/changes
- `refactor:` for code refactoring
- `style:` for formatting changes

Example: `feat: add intelligent element detection for forms`

### Branch Naming

- `feature/description` for new features
- `fix/description` for bug fixes
- `docs/description` for documentation updates

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/tavily_register

# Run specific test file
pytest tests/unit/test_automation.py

# Run integration tests
pytest tests/integration/
```

### Writing Tests

- Write unit tests for all new functions and classes
- Include integration tests for complete workflows
- Use descriptive test names
- Mock external dependencies (web requests, file operations)

### Test Structure

```python
def test_function_name_should_expected_behavior():
    # Arrange
    setup_test_data()
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result == expected_value
```

## 📚 Documentation

### Code Documentation

- Use docstrings for all public functions and classes
- Follow Google docstring format
- Include type hints for function parameters and return values

Example:
```python
def generate_email(email_prefix: str = None) -> str:
    """Generate a random email address.
    
    Args:
        email_prefix: Optional email prefix. If None, uses default from config.
        
    Returns:
        Generated email address string.
        
    Raises:
        ValueError: If email_prefix is invalid.
    """
```

### Documentation Updates

- Update relevant documentation when making changes
- Add examples for new features
- Keep README.md current with new functionality

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - Python version
   - Operating system
   - Browser version (if relevant)

2. **Steps to Reproduce**
   - Clear, numbered steps
   - Expected vs actual behavior
   - Screenshots if helpful

3. **Error Messages**
   - Full error traceback
   - Log files if available

## 💡 Feature Requests

For new features:

1. **Check Existing Issues** - Avoid duplicates
2. **Describe the Problem** - What need does this address?
3. **Propose a Solution** - How should it work?
4. **Consider Alternatives** - Are there other approaches?

## 🔄 Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Follow coding standards
   - Add tests for new functionality
   - Update documentation

3. **Test Your Changes**
   ```bash
   pytest
   black src/ tests/
   isort src/ tests/
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Use descriptive title and description
   - Reference related issues
   - Include testing information

### Pull Request Checklist

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] No merge conflicts
- [ ] Feature/fix is complete

## 🏗️ Project Structure

Understanding the codebase:

- `src/tavily_register/`: Main application code
- `tests/`: Test files
- `docs/`: Documentation
- `scripts/`: Utility scripts
- `examples/`: Usage examples

## 🤝 Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## 📞 Getting Help

- Create an issue for bugs or feature requests
- Join discussions in existing issues
- Check documentation in the `docs/` directory

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

Thank you for contributing to Tavily Register!
