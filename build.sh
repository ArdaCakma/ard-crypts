#!/usr/bin/env bash
# Hata durumunda dur
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate