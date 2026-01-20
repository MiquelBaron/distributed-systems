#!/bin/sh
set -e

# Django ya reconecta automáticamente
python manage.py makemigrations --noinput
python manage.py migrate --noinput

exec "$@"