import os
import re
import shutil
import subprocess
from pathlib import Path


def update_version(file_path, current_version):
    # Parse current version
    major, minor, patch, *rest = current_version.split('.')
    if 'dev' in patch:
        patch = patch.split('dev')[0]

    # Increment minor version
    new_minor = str(int(minor) + 1)
    new_version = f"{major}.{new_minor}.{patch}"
    if 'dev' in current_version:
        new_version += '.dev0'

    # Read file content
    with open(file_path, 'r') as f:
        content = f.read()

    # Update version
    if file_path.endswith('pyproject.toml'):
        content = re.sub(r'version = ".*"',
                         f'version = "{new_version}"', content)
    else:  # setup.py
        content = re.sub(r'version=".*"', f'version="{new_version}"', content)

    # Write back to file
    with open(file_path, 'w') as f:
        f.write(content)

    return new_version


def main():
    # Get current version from pyproject.toml
    with open('pyproject.toml', 'r') as f:
        content = f.read()
    current_version = re.search(r'version = "(.*)"', content).group(1)

    # Update versions
    new_version = update_version('pyproject.toml', current_version)
    update_version('setup.py', current_version)
    print(f"Updated version to {new_version}")

    # Clean dist directory
    dist_dir = Path('dist')
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    print("Cleaned dist directory")

    # Build package
    subprocess.run(['python', '-m', 'build'], check=True)
    print("Built package")

    # Upload with twine
    subprocess.run(['twine', 'upload', 'dist/*'], check=True)
    print("Uploaded package to PyPI")


if __name__ == '__main__':
    main()
