#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Activate virtual environment if needed (if using virtualenv)
# source /path/to/your/venv/bin/activate

# Ensure Python is installed
if ! command -v python3.9 &> /dev/null
then
    echo "Python3.9 could not be found, attempting to install pip and packages..."
    # Try installing pip and dependencies
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.9
    python3.9 -m pip install -r requirements.txt
fi

# Collect static files
echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput

# Create output directory if it doesn't exist
mkdir -p staticfiles_build

# Copy static files to output directory
cp -r static/* staticfiles_build/
