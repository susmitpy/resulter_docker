#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate
python manage.py initadmin
python manage.py site_config

# Start server
echo "Starting server"
gunicorn resulter.wsgi -b 0.0.0.0:8000
