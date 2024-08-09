 echo "BUILD START"
 
 
# Run Django's collectstatic command to gather all static files into STATIC_ROOT
python manage.py collectstatic --noinput
python3.9 -m pip install -r requirements.txt
# Ensure that the output directory exists and move static files there
mkdir -p staticfiles_build
cp -r static/* staticfiles_build/
echo "BUILD END"