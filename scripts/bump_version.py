#!/usr/bin/env python3
"""
Version bump script for VBaaS Python SDK.
Updates version in both pyproject.toml and setup.py files.
"""

import re
import sys
from pathlib import Path


def update_pyproject_toml(version):
    """Update version in pyproject.toml"""
    pyproject_path = Path("pyproject.toml")

    if not pyproject_path.exists():
        print("Error: pyproject.toml not found")
        return False

    content = pyproject_path.read_text()

    # Update version in [project] section
    pattern = r'(version\s*=\s*)"[^"]*"'
    replacement = rf'\1"{version}"'

    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        pyproject_path.write_text(content)
        print(f"Updated version to {version} in pyproject.toml")
        return True
    else:
        print("Error: Could not find version in pyproject.toml")
        return False


def update_setup_py(version):
    """Update version in setup.py"""
    setup_path = Path("setup.py")

    if not setup_path.exists():
        print("Error: setup.py not found")
        return False

    content = setup_path.read_text()

    # Update version in setup() call
    pattern = r'(version\s*=\s*)"[^"]*"'
    replacement = rf'\1"{version}"'

    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        setup_path.write_text(content)
        print(f"Updated version to {version} in setup.py")
        return True
    else:
        print("Error: Could not find version in setup.py")
        return False


def validate_version(version):
    """Validate version format (semantic versioning)"""
    pattern = r"^\d+\.\d+\.\d+$"
    if not re.match(pattern, version):
        print("Error: Version must be in format X.Y.Z (e.g., 1.0.0)")
        return False
    return True


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/bump_version.py <version>")
        print("Example: python scripts/bump_version.py 1.0.1")
        sys.exit(1)

    version = sys.argv[1]

    if not validate_version(version):
        sys.exit(1)

    success = True
    success &= update_pyproject_toml(version)
    success &= update_setup_py(version)

    if success:
        print(f"\n✅ Successfully updated version to {version}")
        print("Next steps:")
        print("1. git add pyproject.toml setup.py")
        print("2. git commit -m 'Bump version to {version}'")
        print("3. git push")
        print("4. Create GitHub release with tag v{version}")
    else:
        print("\n❌ Failed to update version")
        sys.exit(1)


if __name__ == "__main__":
    main()
