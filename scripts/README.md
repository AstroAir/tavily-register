# Scripts Directory

This directory contains utility scripts for development and deployment.

## Scripts

- **setup.py**: Installation and setup script for dependencies and environment
- **dev_setup.py**: Development environment setup (to be created)

## Usage

### Setup Script
Run the setup script to install all dependencies and configure the environment:

```bash
python scripts/setup.py
```

This script will:
- Check Python version compatibility (3.12+)
- Install Python dependencies using pip
- Install Playwright browsers (Firefox by default)
- Create environment configuration files
- Run basic tests to verify installation

**Note**: The setup script now uses `pip install -e .` instead of requirements.txt for better package management.

### Development Setup
For development environment setup (future enhancement):

```bash
python scripts/dev_setup.py  # To be implemented
```

This will install additional development dependencies and configure development tools.

## Script Details

### setup.py Features
- **Automated Installation**: Complete hands-off setup process
- **Error Handling**: Graceful failure handling with helpful error messages
- **Progress Reporting**: Clear status updates throughout the process
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Validation**: Verifies installation success with import tests

### Output Example
```
🚀 开始Tavily自动注册工具安装...
==================================================
🐍 检查Python版本...
✅ Python版本: 3.12.0
📦 安装Python依赖...
✅ 安装项目及依赖 完成
🌐 安装Playwright浏览器...
✅ 安装Chromium浏览器 完成
🧪 运行基础测试...
✅ 所有核心模块导入成功
==================================================
🎉 安装完成！
```

## Troubleshooting

### Common Issues
1. **Python Version**: Ensure Python 3.12+ is installed
2. **Permissions**: Run with appropriate permissions for package installation
3. **Network**: Ensure stable internet connection for downloads
4. **Dependencies**: Some systems may require additional system dependencies

### Manual Fallback
If automated setup fails:
```bash
# Manual installation steps
pip install -e .
playwright install firefox
cp .env.example .env
```

## Development Guidelines

When modifying scripts:
1. **Maintain compatibility** across operating systems
2. **Include comprehensive error handling**
3. **Provide clear progress indicators**
4. **Test on multiple platforms**
5. **Update documentation** when changing functionality
