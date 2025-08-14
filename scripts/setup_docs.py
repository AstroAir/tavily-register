#!/usr/bin/env python3
"""
Documentation Setup Script for Tavily Register

This script sets up the local development environment for documentation,
including MkDocs installation, dependency management, and local server setup.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import List, Optional


class DocumentationSetup:
    """Setup and manage documentation development environment."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.docs_dir = self.project_root / "docs"
        self.site_dir = self.project_root / "site"
        self.python_executable = sys.executable
        
    def check_python_version(self) -> bool:
        """Check if Python version is compatible."""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 12):
            print("❌ Python 3.12+ is required for documentation setup")
            print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
            return False
        
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    
    def install_dependencies(self) -> bool:
        """Install documentation dependencies."""
        print("📦 Installing documentation dependencies...")
        
        try:
            # Install docs dependencies
            cmd = [self.python_executable, "-m", "pip", "install", "-e", ".[docs]"]
            result = subprocess.run(cmd, cwd=self.project_root, check=True, 
                                  capture_output=True, text=True)
            print("✅ Documentation dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print(f"   stdout: {e.stdout}")
            print(f"   stderr: {e.stderr}")
            return False
    
    def setup_git_hooks(self) -> bool:
        """Setup git hooks for documentation."""
        print("🔗 Setting up git hooks...")
        
        hooks_dir = self.project_root / ".git" / "hooks"
        if not hooks_dir.exists():
            print("⚠️  Git repository not found, skipping git hooks setup")
            return True
        
        # Pre-commit hook for documentation validation
        pre_commit_hook = hooks_dir / "pre-commit"
        hook_content = """#!/bin/bash
# Documentation validation pre-commit hook

echo "🔍 Validating documentation..."

# Check if docs files are modified
if git diff --cached --name-only | grep -E "^docs/|mkdocs.yml"; then
    echo "📚 Documentation files modified, running validation..."
    
    # Build documentation to check for errors
    if ! mkdocs build --clean --strict; then
        echo "❌ Documentation build failed!"
        echo "   Please fix the errors before committing."
        exit 1
    fi
    
    echo "✅ Documentation validation passed"
fi

exit 0
"""
        
        try:
            with open(pre_commit_hook, 'w') as f:
                f.write(hook_content)
            
            # Make executable on Unix systems
            if platform.system() != "Windows":
                os.chmod(pre_commit_hook, 0o755)
            
            print("✅ Git hooks setup completed")
            return True
            
        except Exception as e:
            print(f"⚠️  Failed to setup git hooks: {e}")
            return False
    
    def create_local_config(self) -> bool:
        """Create local configuration files."""
        print("⚙️  Creating local configuration...")
        
        # Create local MkDocs config for development
        local_config = self.project_root / "mkdocs.local.yml"
        config_content = """# Local MkDocs configuration for development
INHERIT: mkdocs.yml

# Development-specific settings
dev_addr: '127.0.0.1:8000'
use_directory_urls: false

# Disable plugins that might slow down development
plugins:
  - search
  - awesome-pages
  - macros
  - include-markdown

# Enable live reload for all file types
watch:
  - docs/
  - mkdocs.yml
  - mkdocs.local.yml

# Development theme settings
theme:
  features:
    - navigation.instant.prefetch  # Disable for faster reload
"""
        
        try:
            with open(local_config, 'w') as f:
                f.write(config_content)
            
            print("✅ Local configuration created")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create local config: {e}")
            return False
    
    def validate_setup(self) -> bool:
        """Validate the documentation setup."""
        print("🔍 Validating documentation setup...")
        
        try:
            # Test MkDocs build
            cmd = ["mkdocs", "build", "--clean", "--strict"]
            result = subprocess.run(cmd, cwd=self.project_root, check=True,
                                  capture_output=True, text=True)
            
            print("✅ Documentation builds successfully")
            
            # Check if site directory was created
            if self.site_dir.exists():
                print("✅ Site directory created")
                
                # Count generated files
                html_files = list(self.site_dir.rglob("*.html"))
                print(f"✅ Generated {len(html_files)} HTML files")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Documentation build failed: {e}")
            print(f"   stderr: {e.stderr}")
            return False
    
    def start_dev_server(self, port: int = 8000, host: str = "127.0.0.1") -> None:
        """Start the development server."""
        print(f"🚀 Starting development server at http://{host}:{port}")
        print("   Press Ctrl+C to stop the server")
        
        try:
            cmd = ["mkdocs", "serve", "--dev-addr", f"{host}:{port}"]
            subprocess.run(cmd, cwd=self.project_root)
            
        except KeyboardInterrupt:
            print("\n👋 Development server stopped")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to start server: {e}")
    
    def clean_build(self) -> bool:
        """Clean build artifacts."""
        print("🧹 Cleaning build artifacts...")
        
        try:
            if self.site_dir.exists():
                import shutil
                shutil.rmtree(self.site_dir)
                print("✅ Site directory cleaned")
            
            # Clean Python cache
            cache_dirs = list(self.project_root.rglob("__pycache__"))
            for cache_dir in cache_dirs:
                if cache_dir.is_dir():
                    import shutil
                    shutil.rmtree(cache_dir)
            
            print("✅ Cache directories cleaned")
            return True
            
        except Exception as e:
            print(f"❌ Failed to clean build: {e}")
            return False
    
    def run_setup(self) -> bool:
        """Run the complete setup process."""
        print("🚀 Setting up Tavily Register Documentation")
        print("=" * 50)
        
        steps = [
            ("Checking Python version", self.check_python_version),
            ("Installing dependencies", self.install_dependencies),
            ("Setting up git hooks", self.setup_git_hooks),
            ("Creating local config", self.create_local_config),
            ("Validating setup", self.validate_setup),
        ]
        
        for step_name, step_func in steps:
            print(f"\n{step_name}...")
            if not step_func():
                print(f"❌ Setup failed at: {step_name}")
                return False
        
        print("\n" + "=" * 50)
        print("🎉 Documentation setup completed successfully!")
        print("\nNext steps:")
        print("  1. Run 'python scripts/setup_docs.py serve' to start development server")
        print("  2. Edit documentation files in the 'docs/' directory")
        print("  3. View changes at http://127.0.0.1:8000")
        print("  4. Run 'mkdocs build' to generate static site")
        
        return True


def main():
    """Main entry point."""
    setup = DocumentationSetup()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "serve":
            port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
            setup.start_dev_server(port=port)
        elif command == "build":
            setup.validate_setup()
        elif command == "clean":
            setup.clean_build()
        elif command == "install":
            setup.install_dependencies()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: serve, build, clean, install")
            sys.exit(1)
    else:
        # Run full setup
        success = setup.run_setup()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
