#!/usr/bin/env python3
"""
Version management script for Tavily Register.

This script helps manage package versioning including:
- Reading current version
- Bumping version numbers
- Validating version format
- Updating version in all relevant files
"""
import re
import sys
import argparse
from pathlib import Path
from typing import Tuple, Optional


class VersionManager:
    """Manages package versioning."""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.pyproject_file = self.project_root / "pyproject.toml"
        self.init_file = self.project_root / "src" / "tavily_register" / "__init__.py"
        
    def get_current_version(self) -> Optional[str]:
        """Get the current version from pyproject.toml."""
        try:
            with open(self.pyproject_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find version line
            version_match = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
            if version_match:
                return version_match.group(1)
            
            print("❌ Version not found in pyproject.toml")
            return None
            
        except FileNotFoundError:
            print(f"❌ File not found: {self.pyproject_file}")
            return None
        except Exception as e:
            print(f"❌ Error reading version: {e}")
            return None

    def validate_version(self, version: str) -> bool:
        """Validate version format (semantic versioning)."""
        # Basic semantic versioning pattern: MAJOR.MINOR.PATCH
        pattern = r'^\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)?(?:\+[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)?$'
        
        if re.match(pattern, version):
            print(f"✅ Version format is valid: {version}")
            return True
        else:
            print(f"❌ Invalid version format: {version}")
            print("   Expected format: MAJOR.MINOR.PATCH[-prerelease][+build]")
            return False

    def parse_version(self, version: str) -> Tuple[int, int, int, Optional[str], Optional[str]]:
        """Parse version into components."""
        # Split on + for build metadata
        if '+' in version:
            version, build = version.split('+', 1)
        else:
            build = None
        
        # Split on - for prerelease
        if '-' in version:
            version, prerelease = version.split('-', 1)
        else:
            prerelease = None
        
        # Parse major.minor.patch
        parts = version.split('.')
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        
        return major, minor, patch, prerelease, build

    def format_version(self, major: int, minor: int, patch: int, 
                      prerelease: Optional[str] = None, 
                      build: Optional[str] = None) -> str:
        """Format version components into version string."""
        version = f"{major}.{minor}.{patch}"
        
        if prerelease:
            version += f"-{prerelease}"
        
        if build:
            version += f"+{build}"
        
        return version

    def bump_version(self, bump_type: str, prerelease: Optional[str] = None) -> Optional[str]:
        """Bump version based on type."""
        current = self.get_current_version()
        if not current:
            return None
        
        major, minor, patch, current_prerelease, build = self.parse_version(current)
        
        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
            prerelease = None
        elif bump_type == "minor":
            minor += 1
            patch = 0
            prerelease = None
        elif bump_type == "patch":
            patch += 1
            prerelease = None
        elif bump_type == "prerelease":
            if prerelease is None:
                print("❌ Prerelease identifier required for prerelease bump")
                return None
            # Keep current version numbers, just update prerelease
            pass
        else:
            print(f"❌ Invalid bump type: {bump_type}")
            return None
        
        new_version = self.format_version(major, minor, patch, prerelease, build)
        
        if not self.validate_version(new_version):
            return None
        
        print(f"📈 Version bump: {current} → {new_version}")
        return new_version

    def update_pyproject_version(self, new_version: str) -> bool:
        """Update version in pyproject.toml."""
        try:
            with open(self.pyproject_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace version line
            new_content = re.sub(
                r'^version\s*=\s*["\'][^"\']+["\']',
                f'version = "{new_version}"',
                content,
                flags=re.MULTILINE
            )
            
            with open(self.pyproject_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Updated version in {self.pyproject_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating pyproject.toml: {e}")
            return False

    def update_init_version(self, new_version: str) -> bool:
        """Update version in __init__.py."""
        try:
            if not self.init_file.exists():
                # Create __init__.py with version
                content = f'"""Tavily Register package."""\n\n__version__ = "{new_version}"\n'
            else:
                with open(self.init_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update or add version
                if '__version__' in content:
                    content = re.sub(
                        r'__version__\s*=\s*["\'][^"\']+["\']',
                        f'__version__ = "{new_version}"',
                        content
                    )
                else:
                    # Add version at the end
                    content += f'\n__version__ = "{new_version}"\n'
            
            with open(self.init_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Updated version in {self.init_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating __init__.py: {e}")
            return False

    def set_version(self, new_version: str) -> bool:
        """Set a specific version."""
        if not self.validate_version(new_version):
            return False
        
        current = self.get_current_version()
        if current == new_version:
            print(f"ℹ️  Version is already {new_version}")
            return True
        
        print(f"🔄 Setting version: {current} → {new_version}")
        
        success = (
            self.update_pyproject_version(new_version) and
            self.update_init_version(new_version)
        )
        
        if success:
            print(f"✅ Version updated to {new_version}")
        
        return success

    def show_version_info(self) -> None:
        """Show current version information."""
        current = self.get_current_version()
        if not current:
            return
        
        print(f"📋 Current version: {current}")
        
        try:
            major, minor, patch, prerelease, build = self.parse_version(current)
            print(f"   Major: {major}")
            print(f"   Minor: {minor}")
            print(f"   Patch: {patch}")
            if prerelease:
                print(f"   Prerelease: {prerelease}")
            if build:
                print(f"   Build: {build}")
        except Exception as e:
            print(f"   ⚠️  Could not parse version: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Manage package version")
    subparsers = parser.add_subparsers(dest="command", help="Version commands")
    
    # Show command
    subparsers.add_parser("show", help="Show current version")
    
    # Set command
    set_parser = subparsers.add_parser("set", help="Set specific version")
    set_parser.add_argument("version", help="Version to set (e.g., 1.2.3)")
    
    # Bump command
    bump_parser = subparsers.add_parser("bump", help="Bump version")
    bump_parser.add_argument(
        "type",
        choices=["major", "minor", "patch", "prerelease"],
        help="Type of version bump"
    )
    bump_parser.add_argument(
        "--prerelease",
        help="Prerelease identifier (e.g., alpha, beta, rc1)"
    )
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate version format")
    validate_parser.add_argument("version", help="Version to validate")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    manager = VersionManager()
    
    if args.command == "show":
        manager.show_version_info()
        
    elif args.command == "set":
        success = manager.set_version(args.version)
        sys.exit(0 if success else 1)
        
    elif args.command == "bump":
        new_version = manager.bump_version(args.type, args.prerelease)
        if new_version:
            success = manager.set_version(new_version)
            sys.exit(0 if success else 1)
        else:
            sys.exit(1)
            
    elif args.command == "validate":
        valid = manager.validate_version(args.version)
        sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
