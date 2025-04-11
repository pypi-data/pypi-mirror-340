#!/usr/bin/env python3
"""
VT.ai - Release automation script
This script handles:
1. Version bumping in pyproject.toml
2. Building distribution packages
3. Uploading to PyPI
4. Generating a changelog from git commits
5. Creating a git tag for the release
6. Pushing changes to GitHub
"""

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(command, description=None):
    """Run a shell command and print its output"""
    print(f"\n{'=' * 50}")
    if description:
        print(f"{description}...")
    print(f"Running: {command}")
    print("=" * 50)

    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)

    return result.stdout.strip()


def get_current_version():
    """Get the current version from pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    version_match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if version_match:
        return version_match.group(1)
    raise ValueError("Could not find version in pyproject.toml")


def update_version(new_version):
    """Update the version in pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    updated_content = re.sub(
        r'version\s*=\s*"([^"]+)"', f'version = "{new_version}"', content
    )
    pyproject_path.write_text(updated_content)
    print(f"Version updated to {new_version} in pyproject.toml")


def get_commit_history(previous_tag=None, current_tag=None):
    """Get commit history since the last tag or between specified tags"""
    if not previous_tag:
        # Get the most recent tag if not specified
        try:
            previous_tag = run_command(
                "git describe --tags --abbrev=0", "Finding the most recent tag"
            )
        except:
            # If no tags exist yet, get all commits
            print("No previous tags found. Including all commits in changelog.")
            return run_command(
                "git log --pretty=format:'%h %s (%an)' --no-merges",
                "Getting all commit history",
            )

    range_spec = f"{previous_tag}..HEAD"
    if current_tag:
        range_spec = f"{previous_tag}..{current_tag}"

    return run_command(
        f"git log {range_spec} --pretty=format:'%h %s (%an)' --no-merges",
        f"Getting commit history from {range_spec}",
    )


def generate_changelog(new_version, previous_tag=None):
    """Generate a changelog from git commit history"""
    print("\nGenerating changelog...")

    changelog_path = Path("CHANGELOG.md")
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Get commit history
    commit_history = get_commit_history(previous_tag)
    if not commit_history:
        print("No new commits found for changelog.")
        return changelog_path

    # Create categorized commits if possible
    feature_commits = []
    fix_commits = []
    other_commits = []

    for line in commit_history.split("\n"):
        if not line.strip():
            continue
        if re.search(r"(feat|feature|add)[\(\):]", line.lower()):
            feature_commits.append(line)
        elif re.search(r"(fix|bug|patch)[\(\):]", line.lower()):
            fix_commits.append(line)
        else:
            other_commits.append(line)

    # Generate changelog content
    changelog_content = f"## v{new_version} ({current_date})\n\n"

    if feature_commits:
        changelog_content += "### Features\n\n"
        for commit in feature_commits:
            changelog_content += f"- {commit}\n"
        changelog_content += "\n"

    if fix_commits:
        changelog_content += "### Bug Fixes\n\n"
        for commit in fix_commits:
            changelog_content += f"- {commit}\n"
        changelog_content += "\n"

    if other_commits:
        changelog_content += "### Other Changes\n\n"
        for commit in other_commits:
            changelog_content += f"- {commit}\n"
        changelog_content += "\n"

    # Update or create the changelog file
    if changelog_path.exists():
        existing_content = changelog_path.read_text()
        changelog_path.write_text(changelog_content + existing_content)
    else:
        changelog_path.write_text(f"# Changelog\n\n{changelog_content}")

    print(f"Changelog updated at {changelog_path}")
    return changelog_path


def get_git_remote():
    """Get the default git remote (usually 'origin')"""
    try:
        remotes = run_command("git remote", "Listing git remotes")
        if not remotes:
            print("No git remotes found. Using 'origin' as default.")
            return "origin"

        # If multiple remotes, prefer 'origin'
        if "origin" in remotes.split("\n"):
            return "origin"
        # Otherwise use the first remote
        return remotes.split("\n")[0]
    except:
        print("Error getting git remotes. Using 'origin' as default.")
        return "origin"


def main():
    # 1. Get current version and ask for new version
    current_version = get_current_version()
    print(f"Current version: {current_version}")
    new_version = input("Enter new version number (or press Enter to keep current): ")

    if not new_version:
        new_version = current_version
        print(f"Keeping version at {current_version}")
    else:
        # Update version in pyproject.toml
        update_version(new_version)

    # 2. Generate changelog
    try:
        # Try to get the last tag for changelog generation
        last_tag = run_command(
            "git describe --tags --abbrev=0", "Getting last tag for changelog"
        )
    except:
        last_tag = None

    changelog_path = generate_changelog(new_version, last_tag)

    # 3. Build distribution packages
    run_command(
        "python -m pip install --upgrade build twine",
        "Installing/upgrading build and twine",
    )
    run_command("rm -rf dist/*", "Cleaning dist directory")
    run_command("python -m build", "Building distribution packages")

    # 4. Upload to PyPI
    upload = input("Upload to PyPI? (y/n): ").lower()
    if upload == "y":
        run_command("python -m twine upload dist/*", "Uploading to PyPI")

    # 5. Create git commit with version and changelog
    run_command("git add pyproject.toml", "Staging pyproject.toml changes")
    run_command(f"git add {changelog_path}", "Staging changelog changes")
    run_command(
        f'git commit -m "Bump version to {new_version}"', "Committing version change"
    )
    run_command(
        f'git tag -a v{new_version} -m "Version {new_version}"', "Creating git tag"
    )

    # 6. Push changes and tags to GitHub
    push = input("Push changes to GitHub? (y/n): ").lower()
    if push == "y":
        # Get default remote
        remote = get_git_remote()
        run_command(f"git push {remote}", "Pushing commits")
        run_command(f"git push {remote} --tags", "Pushing tags")

    print("\n✅ Release process completed successfully!")


if __name__ == "__main__":
    main()
