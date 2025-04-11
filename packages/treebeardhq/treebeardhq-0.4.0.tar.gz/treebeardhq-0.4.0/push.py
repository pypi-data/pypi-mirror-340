import os
import re
import shutil
import subprocess
import argparse
from pathlib import Path


def update_version(file_path, current_version, is_dev):
    # Parse current version
    major, minor, patch, *rest = current_version.split('.')
    if 'dev' in patch:
        patch, dev = patch.split('dev')
    else:
        dev = None

    if is_dev and dev is not None:
        # Increment dev version
        new_dev = str(int(dev) + 1)
        new_version = f"{major}.{minor}.{patch}dev{new_dev}"
    else:
        # Increment minor version
        new_minor = str(int(minor) + 1)
        new_version = f"{major}.{new_minor}.{patch}"
        if dev is not None:
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
    parser = argparse.ArgumentParser(description='Push package to PyPI')
    parser.add_argument('--dev', action='store_true',
                        help='Increment dev version instead of minor version')
    args = parser.parse_args()

    # Get current version from pyproject.toml
    with open('pyproject.toml', 'r') as f:
        content = f.read()
    current_version = re.search(r'version = "(.*)"', content).group(1)

    # Update versions
    new_version = update_version('pyproject.toml', current_version, args.dev)
    update_version('setup.py', current_version, args.dev)
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
