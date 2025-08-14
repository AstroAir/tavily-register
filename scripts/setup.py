#!/usr/bin/env python3
"""
项目安装和设置脚本
"""
import subprocess
import sys
import os

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e}")
        if e.stdout:
            print(f"输出: {e.stdout}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print("需要Python 3.7或更高版本")
        return False

def install_dependencies():
    """安装Python依赖"""
    print("\n📦 安装Python依赖...")

    # 升级pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "升级pip"):
        return False

    # 安装项目及其依赖
    if not run_command(f"{sys.executable} -m pip install -e .", "安装项目及依赖"):
        return False

    return True

def install_playwright():
    """安装Playwright浏览器"""
    print("\n🌐 安装Playwright浏览器...")
    
    if not run_command("playwright install chromium", "安装Chromium浏览器"):
        return False
    
    return True

def create_env_file():
    """创建.env文件"""
    print("\n⚙️ 创建环境配置文件...")
    
    if os.path.exists('.env'):
        print("✅ .env文件已存在")
        return True
    
    if os.path.exists('.env.example'):
        try:
            with open('.env.example', 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ 已从.env.example创建.env文件")
            return True
        except Exception as e:
            print(f"❌ 创建.env文件失败: {e}")
            return False
    else:
        print("⚠️ .env.example文件不存在，跳过.env文件创建")
        return True

def run_basic_test():
    """运行基础测试"""
    print("\n🧪 运行基础测试...")

    # 检查主要模块是否可以导入
    try:
        from src.tavily_register.core.intelligent_automation import IntelligentTavilyAutomation
        from src.tavily_register.email.checker import EmailChecker
        from src.tavily_register.config.settings import EMAIL_DOMAIN
        from src.tavily_register.utils.helpers import generate_email
        print("✅ 所有核心模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def main():
    """主安装函数"""
    print("🚀 开始Tavily自动注册工具安装...")
    print("=" * 50)
    
    steps = [
        ("检查Python版本", check_python_version),
        ("安装Python依赖", install_dependencies),
        ("安装Playwright浏览器", install_playwright),
        ("创建环境配置文件", create_env_file),
        ("运行基础测试", run_basic_test)
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"\n❌ 安装失败于步骤: {step_name}")
            print("请检查错误信息并重试")
            return False
    
    print("\n" + "=" * 50)
    print("🎉 安装完成！")
    print("\n📖 使用说明:")
    print("1. 运行主程序: python main.py")
    print("2. 查看README.md了解详细使用方法")
    print("3. 如需修改配置，请编辑config.py或.env文件")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
