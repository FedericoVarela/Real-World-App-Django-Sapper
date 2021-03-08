#!/usr/bin/env bash
python manage.py migrate --settings=server.settings.production
python manage.py runserver 0.0.0.0:8000 --settings=server.settings.staging