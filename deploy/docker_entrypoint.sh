#!/usr/bin/env bash
python manage.py migrate

service nginx start

gunicorn domain_schema.wsgi:application --name  Schema --workers 3 --bind=unix:/var/www/schema/gunicorn.sock --log-level=debug --log-file=-
