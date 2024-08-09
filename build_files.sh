 echo "BUILD START"
 python3.9 -m pip install -r requirements.txt
 python3.9 manage.py collectstatic --noinput --clear
 echo "BUILD END"

 #!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Run Django's collectstatic command to gather all static files into STATIC_ROOT
python manage.py collectstatic --noinput

# Ensure that the output directory exists and move static files there
mkdir -p staticfiles_build
cp -r static/* staticfiles_build/
