# Release Process

This document describes the complete release process for Tavily Register, including version management, testing, and distribution.

## Overview

The release process is automated using GitHub Actions and includes:

1. **Version Management**: Semantic versioning with automated updates
2. **Testing**: Comprehensive testing across multiple platforms
3. **Building**: Automated package building and validation
4. **Publishing**: Secure publishing to PyPI using trusted publishing
5. **Documentation**: Automated changelog and release notes

## Prerequisites

### Repository Setup

1. **Trusted Publishing Configuration**:
   - Configure trusted publishing on [PyPI](https://pypi.org/manage/account/publishing/)
   - Configure trusted publishing on [TestPyPI](https://test.pypi.org/manage/account/publishing/)
   - Set up GitHub environments: `pypi` and `testpypi`

2. **Repository Settings**:
   - Enable GitHub Actions
   - Configure branch protection for `main`
   - Set up required status checks

### Local Development Setup

```bash
# Install development dependencies
pip install -e ".[dev,test,security]"

# Install build tools
pip install build twine check-manifest

# Set up pre-commit hooks
pre-commit install
```

## Release Types

### Patch Release (0.1.0 → 0.1.1)
- Bug fixes
- Documentation updates
- Minor improvements

### Minor Release (0.1.0 → 0.2.0)
- New features
- API additions (backward compatible)
- Significant improvements

### Major Release (0.1.0 → 1.0.0)
- Breaking changes
- Major API changes
- Architectural changes

## Step-by-Step Release Process

### 1. Prepare for Release

```bash
# Ensure you're on the main branch
git checkout main
git pull origin main

# Check current version
python scripts/version.py show

# Review changes since last release
python scripts/release.py info 0.2.0
```

### 2. Update Version

```bash
# Bump version (choose appropriate type)
python scripts/version.py bump patch    # For patch release
python scripts/version.py bump minor    # For minor release
python scripts/version.py bump major    # For major release

# Or set specific version
python scripts/version.py set 0.2.0
```

### 3. Run Local Tests

```bash
# Run comprehensive test suite
python tests/run_comprehensive_tests.py

# Run security scans
bandit -r src/
safety check

# Test local build
python scripts/build.py release
```

### 4. Update Documentation

```bash
# Update changelog (automatic with release script)
python scripts/release.py changelog 0.2.0

# Review and edit CHANGELOG.md if needed
# Update any version-specific documentation
```

### 5. Commit Changes

```bash
# Commit version and changelog updates
git add .
git commit -m "chore: prepare release v0.2.0"
git push origin main
```

### 6. Create Release

```bash
# Prepare release (creates tag)
python scripts/release.py prepare 0.2.0

# Push tag to trigger release workflow
git push origin v0.2.0
```

### 7. Monitor Release

1. **GitHub Actions**: Monitor the release workflow
2. **TestPyPI**: Verify package appears on TestPyPI
3. **PyPI**: Verify package appears on PyPI (for tagged releases)
4. **GitHub Release**: Check that GitHub release is created

### 8. Post-Release Verification

```bash
# Test installation from PyPI
pip install tavily-register==0.2.0

# Verify functionality
tavily-register --help
python -c "import tavily_register; print(tavily_register.__version__)"
```

## Automated Workflows

### CI/CD Pipeline (`.github/workflows/ci.yml`)

Runs on every push and pull request:
- Code quality checks (Black, Flake8, MyPy)
- Security scanning (Bandit, Safety)
- Multi-platform testing
- Coverage analysis
- Performance benchmarks

### Build Workflow (`.github/workflows/build.yml`)

Runs on pushes to main and tags:
- Package validation
- Build source and wheel distributions
- Package integrity checks
- Installation testing

### Distribution Testing (`.github/workflows/test-distribution.yml`)

Tests package distribution:
- Package building
- Installation in clean environments
- Metadata validation
- Entry point testing

### Publishing Workflow (`.github/workflows/publish.yml`)

Triggered by tags or manual dispatch:
- Builds packages
- Publishes to TestPyPI (always)
- Publishes to PyPI (tagged releases only)
- Creates GitHub releases
- Generates release notes

## Manual Release (Emergency)

If automated release fails, you can release manually:

```bash
# Build package
python -m build

# Check package
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI (after verification)
twine upload dist/*
```

## Rollback Procedure

If a release has issues:

1. **Immediate**: Yank the problematic version on PyPI
2. **Fix**: Create a patch release with fixes
3. **Communicate**: Update documentation and notify users

```bash
# Yank version on PyPI (if needed)
# This must be done through PyPI web interface

# Create hotfix
python scripts/version.py bump patch
# Fix the issue
git commit -m "fix: critical issue in v0.2.0"
python scripts/release.py prepare 0.2.1 --push
```

## Best Practices

### Version Management
- Follow semantic versioning strictly
- Update version in all relevant files
- Tag releases consistently

### Testing
- Always run full test suite before release
- Test installation from built packages
- Verify functionality in clean environments

### Documentation
- Keep CHANGELOG.md up to date
- Update version-specific documentation
- Include migration guides for breaking changes

### Security
- Use trusted publishing (no API tokens)
- Scan for vulnerabilities before release
- Keep dependencies updated

### Communication
- Write clear release notes
- Announce significant releases
- Provide upgrade instructions

## Troubleshooting

### Common Issues

1. **Version Mismatch**: Ensure tag version matches package version
2. **Build Failures**: Check pyproject.toml configuration
3. **Upload Failures**: Verify trusted publishing setup
4. **Test Failures**: Run tests locally first

### Getting Help

- Check GitHub Actions logs
- Review workflow files
- Consult PyPI documentation
- Check trusted publishing configuration

## Tools and Scripts

- `scripts/version.py`: Version management
- `scripts/release.py`: Release preparation
- `scripts/build.py`: Local building and testing
- `tests/run_comprehensive_tests.py`: Test execution

## References

- [Python Packaging User Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
