#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting build script..."

# Check if Python 3.9 is available
if ! command -v python3.9 &> /dev/null; then
    echo "Error: Python 3.9 is not installed."
    exit 1
fi

# Install pip if it is not available
if ! python3.9 -m pip &> /dev/null; then
    echo "Pip is not installed. Installing pip..."
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.9 || { echo 'Failed to install pip'; exit 1; }
fi

# Install Python dependencies
echo "Installing dependencies..."
python3.9 -m pip install -r requirements.txt || { echo 'Failed to install dependencies'; exit 1; }

# Collect static files
echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput || { echo 'Collectstatic failed'; exit 1; }

# Create output directory if it doesn't exist
echo "Creating staticfiles_build directory..."
mkdir -p staticfiles_build

# Copy static files to output directory
echo "Copying static files to output directory..."
cp -r static/* staticfiles_build/ || { echo 'Failed to copy static files'; exit 1; }

echo "Build script executed successfully."
