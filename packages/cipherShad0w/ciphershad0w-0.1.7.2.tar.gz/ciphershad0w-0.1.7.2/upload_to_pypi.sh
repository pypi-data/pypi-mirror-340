#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Step 1: Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

# Step 2: Build the package
echo "Building the package..."
python setup.py sdist bdist_wheel

# Step 3: Upload the package to PyPI
echo "Uploading the package to PyPI..."
twine upload dist/*

echo "Upload to PyPI completed successfully!"
