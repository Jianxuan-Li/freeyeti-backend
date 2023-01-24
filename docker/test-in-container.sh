#!/bin/sh
mkdir -p /data/logs
mkdir -p /data/attachments

if [ -f "$DJANGO_LOG_FILE" ]; then
    echo "$DJANGO_LOG_FILE exists."
else 
    touch $DJANGO_LOG_FILE
    echo "$DJANGO_LOG_FILE does not exist. created"
fi

poetry install
poetry run python manage.py migrate
poetry run coverage run --source='.' manage.py test
poetry run coverage report
