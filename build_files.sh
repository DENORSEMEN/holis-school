#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Activate virtual environment if needed (uncomment and specify path if using virtualenv)
# source /path/to/your/venv/bin/activate

# Check if Python 3.9 is available
if ! command -v python3.9 &> /dev/null; then
    echo "Error: Python 3.9 is not installed."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "Pip is not installed. Installing pip..."
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.9
fi

# Install Python dependencies
echo "Installing dependencies..."
python3.9 -m pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput

# Create output directory if it doesn't exist
mkdir -p staticfiles_build

# Copy static files to output directory
echo "Copying static files to output directory..."
cp -r static/* staticfiles_build/

echo "Build script executed successfully."
