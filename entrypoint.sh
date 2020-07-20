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

# AWS EC2 Port 80 to 8000
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8000

# Start server
echo "Starting server"
gunicorn resulter.wsgi -b 0.0.0.0:8000
