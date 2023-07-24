#!/bin/bash

python manage.py migrate --no-input

python manage.py collectstatic --no-input

python manage.py load_from_csv_ingredients

python manage.py load_from_csv_tags

gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000