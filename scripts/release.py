#!/usr/bin/env python3
"""
Release management script for Tavily Register.

This script automates the release process including:
- Version validation
- Changelog generation
- Git tagging
- Release preparation
"""
import subprocess
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any


class ReleaseManager:
    """Manages package releases."""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.changelog_file = self.project_root / "CHANGELOG.md"
        
    def run_command(self, command: str, description: str, check: bool = True) -> tuple[bool, str]:
        """Run a command and return success status and output."""
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
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed: {e}")
            if e.stderr:
                print(f"   Error: {e.stderr}")
            return False, e.stderr or ""

    def get_current_version(self) -> Optional[str]:
        """Get current version from pyproject.toml."""
        try:
            import tomllib
            with open(self.project_root / "pyproject.toml", "rb") as f:
                data = tomllib.load(f)
            return data["project"]["version"]
        except Exception as e:
            print(f"❌ Error reading version: {e}")
            return None

    def validate_git_status(self) -> bool:
        """Validate git repository status."""
        print("🔍 Validating git status...")
        
        # Check if we're in a git repository
        success, _ = self.run_command("git rev-parse --git-dir", "Checking git repository")
        if not success:
            return False
        
        # Check for uncommitted changes
        success, output = self.run_command("git status --porcelain", "Checking for uncommitted changes")
        if not success:
            return False
        
        if output.strip():
            print("❌ Uncommitted changes found:")
            print(output)
            print("   Please commit or stash changes before releasing")
            return False
        
        print("✅ Git status is clean")
        return True

    def get_git_commits_since_tag(self, tag: Optional[str] = None) -> List[str]:
        """Get git commits since the last tag."""
        if tag is None:
            # Get the latest tag
            success, latest_tag = self.run_command(
                "git describe --tags --abbrev=0",
                "Getting latest tag",
                check=False
            )
            if not success:
                # No tags found, get all commits
                success, output = self.run_command(
                    'git log --oneline --pretty=format:"%h %s"',
                    "Getting all commits"
                )
            else:
                # Get commits since latest tag
                success, output = self.run_command(
                    f'git log {latest_tag}..HEAD --oneline --pretty=format:"%h %s"',
                    f"Getting commits since {latest_tag}"
                )
        else:
            success, output = self.run_command(
                f'git log {tag}..HEAD --oneline --pretty=format:"%h %s"',
                f"Getting commits since {tag}"
            )
        
        if not success:
            return []
        
        return [line.strip() for line in output.split('\n') if line.strip()]

    def categorize_commits(self, commits: List[str]) -> Dict[str, List[str]]:
        """Categorize commits by type."""
        categories = {
            'features': [],
            'fixes': [],
            'docs': [],
            'tests': [],
            'chore': [],
            'other': []
        }
        
        for commit in commits:
            commit_lower = commit.lower()
            
            if any(keyword in commit_lower for keyword in ['feat:', 'feature:', 'add:', 'new:']):
                categories['features'].append(commit)
            elif any(keyword in commit_lower for keyword in ['fix:', 'bug:', 'patch:']):
                categories['fixes'].append(commit)
            elif any(keyword in commit_lower for keyword in ['doc:', 'docs:', 'readme:']):
                categories['docs'].append(commit)
            elif any(keyword in commit_lower for keyword in ['test:', 'tests:']):
                categories['tests'].append(commit)
            elif any(keyword in commit_lower for keyword in ['chore:', 'refactor:', 'style:']):
                categories['chore'].append(commit)
            else:
                categories['other'].append(commit)
        
        return categories

    def generate_changelog_entry(self, version: str, commits: List[str]) -> str:
        """Generate changelog entry for the version."""
        date = datetime.now().strftime("%Y-%m-%d")
        categories = self.categorize_commits(commits)
        
        entry = f"## [{version}] - {date}\n\n"
        
        if categories['features']:
            entry += "### ✨ Features\n"
            for commit in categories['features']:
                entry += f"- {commit}\n"
            entry += "\n"
        
        if categories['fixes']:
            entry += "### 🐛 Bug Fixes\n"
            for commit in categories['fixes']:
                entry += f"- {commit}\n"
            entry += "\n"
        
        if categories['docs']:
            entry += "### 📚 Documentation\n"
            for commit in categories['docs']:
                entry += f"- {commit}\n"
            entry += "\n"
        
        if categories['tests']:
            entry += "### 🧪 Tests\n"
            for commit in categories['tests']:
                entry += f"- {commit}\n"
            entry += "\n"
        
        if categories['chore']:
            entry += "### 🔧 Maintenance\n"
            for commit in categories['chore']:
                entry += f"- {commit}\n"
            entry += "\n"
        
        if categories['other']:
            entry += "### 📝 Other Changes\n"
            for commit in categories['other']:
                entry += f"- {commit}\n"
            entry += "\n"
        
        return entry

    def update_changelog(self, version: str, commits: List[str]) -> bool:
        """Update CHANGELOG.md with new version."""
        print(f"📝 Updating changelog for version {version}...")
        
        entry = self.generate_changelog_entry(version, commits)
        
        if not self.changelog_file.exists():
            # Create new changelog
            content = f"# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n{entry}"
        else:
            # Update existing changelog
            with open(self.changelog_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            # Insert new entry after the header
            lines = existing_content.split('\n')
            header_end = 0
            for i, line in enumerate(lines):
                if line.startswith('## [') or (i > 0 and line.strip() == ''):
                    header_end = i
                    break
            
            if header_end == 0:
                # No existing entries, add after header
                content = '\n'.join(lines[:3]) + '\n\n' + entry + '\n'.join(lines[3:])
            else:
                content = '\n'.join(lines[:header_end]) + '\n' + entry + '\n'.join(lines[header_end:])
        
        try:
            with open(self.changelog_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated {self.changelog_file}")
            return True
        except Exception as e:
            print(f"❌ Error updating changelog: {e}")
            return False

    def create_git_tag(self, version: str, message: Optional[str] = None) -> bool:
        """Create and push git tag."""
        tag_name = f"v{version}"
        
        if message is None:
            message = f"Release version {version}"
        
        print(f"🏷️  Creating git tag {tag_name}...")
        
        # Create tag
        success, _ = self.run_command(
            f'git tag -a {tag_name} -m "{message}"',
            f"Creating tag {tag_name}"
        )
        
        if not success:
            return False
        
        print(f"✅ Created tag {tag_name}")
        return True

    def push_tag(self, version: str) -> bool:
        """Push tag to remote repository."""
        tag_name = f"v{version}"
        
        success, _ = self.run_command(
            f"git push origin {tag_name}",
            f"Pushing tag {tag_name}"
        )
        
        if success:
            print(f"✅ Pushed tag {tag_name} to remote")
        
        return success

    def prepare_release(self, version: str, push_tag: bool = False) -> bool:
        """Prepare a release."""
        print(f"🚀 Preparing release for version {version}")
        print("=" * 50)
        
        # Validate git status
        if not self.validate_git_status():
            return False
        
        # Get commits for changelog
        commits = self.get_git_commits_since_tag()
        if not commits:
            print("⚠️  No new commits found since last tag")
        else:
            print(f"📋 Found {len(commits)} commits since last tag")
        
        # Update changelog
        if not self.update_changelog(version, commits):
            return False
        
        # Create git tag
        if not self.create_git_tag(version):
            return False
        
        # Push tag if requested
        if push_tag:
            if not self.push_tag(version):
                print("⚠️  Failed to push tag, but release preparation completed")
        
        print("=" * 50)
        print(f"✅ Release preparation completed for version {version}")
        
        if not push_tag:
            print(f"💡 To push the tag and trigger release, run:")
            print(f"   git push origin v{version}")
        
        return True

    def show_release_info(self, version: str) -> None:
        """Show information about a potential release."""
        print(f"📋 Release Information for v{version}")
        print("=" * 50)
        
        current_version = self.get_current_version()
        print(f"Current version: {current_version}")
        print(f"Target version: {version}")
        
        commits = self.get_git_commits_since_tag()
        if commits:
            print(f"\nCommits since last tag ({len(commits)}):")
            categories = self.categorize_commits(commits)
            
            for category, commit_list in categories.items():
                if commit_list:
                    print(f"\n{category.title()}:")
                    for commit in commit_list[:5]:  # Show first 5
                        print(f"  - {commit}")
                    if len(commit_list) > 5:
                        print(f"  ... and {len(commit_list) - 5} more")
        else:
            print("\nNo new commits since last tag")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Manage package releases")
    subparsers = parser.add_subparsers(dest="command", help="Release commands")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show release information")
    info_parser.add_argument("version", help="Version to show info for")
    
    # Prepare command
    prepare_parser = subparsers.add_parser("prepare", help="Prepare release")
    prepare_parser.add_argument("version", help="Version to release")
    prepare_parser.add_argument("--push", action="store_true", help="Push tag after creation")
    
    # Changelog command
    changelog_parser = subparsers.add_parser("changelog", help="Update changelog only")
    changelog_parser.add_argument("version", help="Version for changelog")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    manager = ReleaseManager()
    
    if args.command == "info":
        manager.show_release_info(args.version)
        
    elif args.command == "prepare":
        success = manager.prepare_release(args.version, args.push)
        sys.exit(0 if success else 1)
        
    elif args.command == "changelog":
        commits = manager.get_git_commits_since_tag()
        success = manager.update_changelog(args.version, commits)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
