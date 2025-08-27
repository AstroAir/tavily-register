#!/usr/bin/env python3
"""
Local build script for Tavily Register package.

This script provides local development build capabilities including:
- Clean builds
- Development builds
- Release builds
- Build validation
- Local testing
"""
import subprocess
import sys
import os
import shutil
import argparse
from pathlib import Path
from typing import Optional


class PackageBuilder:
    """Package builder for local development."""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        
    def run_command(self, command: str, description: str, check: bool = True) -> bool:
        """Run a command and display results."""
        print(f"🔧 {description}...")
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                check=check, 
                capture_output=True, 
                text=True,
                cwd=self.project_root
            )
            if result.stdout:
                print(f"   {result.stdout.strip()}")
            print(f"✅ {description} completed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed: {e}")
            if e.stdout:
                print(f"   Output: {e.stdout}")
            if e.stderr:
                print(f"   Error: {e.stderr}")
            return False

    def clean(self) -> bool:
        """Clean build artifacts."""
        print("🧹 Cleaning build artifacts...")
        
        # Remove directories
        dirs_to_remove = [
            self.dist_dir,
            self.build_dir,
            self.project_root / "src" / "tavily_register.egg-info",
            self.project_root / "htmlcov",
            self.project_root / ".pytest_cache",
            self.project_root / ".mypy_cache",
        ]
        
        for dir_path in dirs_to_remove:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   Removed {dir_path}")
        
        # Remove files
        files_to_remove = [
            self.project_root / "coverage.xml",
            self.project_root / "bandit-report.json",
            self.project_root / "safety-report.json",
        ]
        
        for file_path in files_to_remove:
            if file_path.exists():
                file_path.unlink()
                print(f"   Removed {file_path}")
        
        print("✅ Clean completed")
        return True

    def validate_environment(self) -> bool:
        """Validate the build environment."""
        print("🔍 Validating build environment...")
        
        # Check Python version
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 11):
            print(f"❌ Python 3.11+ required, found {version.major}.{version.minor}")
            return False
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        
        # Check required files
        required_files = [
            "pyproject.toml",
            "README.md",
            "LICENSE",
            "src/tavily_register/__init__.py"
        ]
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                print(f"❌ Missing required file: {file_path}")
                return False
            print(f"✅ Found: {file_path}")
        
        return True

    def install_build_deps(self) -> bool:
        """Install build dependencies."""
        return self.run_command(
            f"{sys.executable} -m pip install build twine check-manifest",
            "Installing build dependencies"
        )

    def validate_config(self) -> bool:
        """Validate package configuration."""
        print("📋 Validating package configuration...")
        
        # Validate pyproject.toml
        try:
            import tomllib
            with open(self.project_root / "pyproject.toml", "rb") as f:
                data = tomllib.load(f)
            
            project = data.get("project", {})
            required_fields = ["name", "version", "description", "authors"]
            
            for field in required_fields:
                if field not in project:
                    print(f"❌ Missing required field in pyproject.toml: {field}")
                    return False
                print(f"✅ {field}: {project[field]}")
                
        except Exception as e:
            print(f"❌ Invalid pyproject.toml: {e}")
            return False
        
        # Check manifest
        return self.run_command("check-manifest", "Checking MANIFEST.in")

    def build_source(self) -> bool:
        """Build source distribution."""
        return self.run_command(
            f"{sys.executable} -m build --sdist",
            "Building source distribution"
        )

    def build_wheel(self) -> bool:
        """Build wheel distribution."""
        return self.run_command(
            f"{sys.executable} -m build --wheel",
            "Building wheel distribution"
        )

    def validate_packages(self) -> bool:
        """Validate built packages."""
        if not self.dist_dir.exists():
            print("❌ No dist directory found")
            return False
        
        packages = list(self.dist_dir.glob("*"))
        if not packages:
            print("❌ No packages found in dist directory")
            return False
        
        print(f"📦 Found {len(packages)} packages:")
        for package in packages:
            size = package.stat().st_size
            print(f"   {package.name} ({size:,} bytes)")
        
        # Validate with twine
        return self.run_command("twine check dist/*", "Validating packages with twine")

    def test_install(self, use_wheel: bool = True) -> bool:
        """Test package installation."""
        print("🧪 Testing package installation...")
        
        # Create temporary virtual environment
        venv_dir = self.project_root / ".test_venv"
        if venv_dir.exists():
            shutil.rmtree(venv_dir)
        
        # Create venv
        if not self.run_command(
            f"{sys.executable} -m venv {venv_dir}",
            "Creating test virtual environment"
        ):
            return False
        
        # Determine Python executable in venv
        if sys.platform == "win32":
            python_exe = venv_dir / "Scripts" / "python.exe"
        else:
            python_exe = venv_dir / "bin" / "python"
        
        try:
            # Install package
            if use_wheel:
                wheel_files = list(self.dist_dir.glob("*.whl"))
                if not wheel_files:
                    print("❌ No wheel files found")
                    return False
                package_file = wheel_files[0]
            else:
                sdist_files = list(self.dist_dir.glob("*.tar.gz"))
                if not sdist_files:
                    print("❌ No source distribution files found")
                    return False
                package_file = sdist_files[0]
            
            if not self.run_command(
                f"{python_exe} -m pip install {package_file}",
                f"Installing {'wheel' if use_wheel else 'source'} package"
            ):
                return False
            
            # Test import
            if not self.run_command(
                f"{python_exe} -c \"import tavily_register; print('✓ Import successful')\"",
                "Testing package import"
            ):
                return False
            
            # Test entry point
            if not self.run_command(
                f"{python_exe} -m tavily_register.main --help",
                "Testing entry point"
            ):
                return False
            
            print("✅ Package installation test passed")
            return True
            
        finally:
            # Cleanup
            if venv_dir.exists():
                shutil.rmtree(venv_dir)

    def build_dev(self) -> bool:
        """Build for development (with validation)."""
        print("🚀 Starting development build...")
        
        steps = [
            ("Validating environment", self.validate_environment),
            ("Installing build dependencies", self.install_build_deps),
            ("Validating configuration", self.validate_config),
            ("Building source distribution", self.build_source),
            ("Building wheel distribution", self.build_wheel),
            ("Validating packages", self.validate_packages),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print(f"❌ Development build failed at: {step_name}")
                return False
        
        print("✅ Development build completed successfully!")
        return True

    def build_release(self) -> bool:
        """Build for release (with full testing)."""
        print("🚀 Starting release build...")
        
        steps = [
            ("Cleaning previous builds", self.clean),
            ("Validating environment", self.validate_environment),
            ("Installing build dependencies", self.install_build_deps),
            ("Validating configuration", self.validate_config),
            ("Building source distribution", self.build_source),
            ("Building wheel distribution", self.build_wheel),
            ("Validating packages", self.validate_packages),
            ("Testing wheel installation", lambda: self.test_install(use_wheel=True)),
            ("Testing source installation", lambda: self.test_install(use_wheel=False)),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print(f"❌ Release build failed at: {step_name}")
                return False
        
        print("✅ Release build completed successfully!")
        print(f"📦 Packages available in: {self.dist_dir}")
        return True


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Build Tavily Register package")
    parser.add_argument(
        "command",
        choices=["clean", "dev", "release", "validate", "test-install"],
        help="Build command to execute"
    )
    parser.add_argument(
        "--wheel-only",
        action="store_true",
        help="Test wheel installation only"
    )
    
    args = parser.parse_args()
    
    builder = PackageBuilder()
    
    if args.command == "clean":
        success = builder.clean()
    elif args.command == "dev":
        success = builder.build_dev()
    elif args.command == "release":
        success = builder.build_release()
    elif args.command == "validate":
        success = (
            builder.validate_environment() and
            builder.validate_config() and
            builder.validate_packages()
        )
    elif args.command == "test-install":
        success = builder.test_install(use_wheel=not args.wheel_only)
    else:
        print(f"Unknown command: {args.command}")
        success = False
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
