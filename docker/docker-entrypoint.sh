#!/bin/sh
mkdir -p /data/cache
mkdir -p /data/logs

if [ -f "$DJANGO_LOG_FILE" ]; then
    echo "$DJANGO_LOG_FILE exists."
else 
    touch $DJANGO_LOG_FILE
    echo "$DJANGO_LOG_FILE does not exist. created"
fi

gunicorn -b 0.0.0.0:8000 freeyeti.wsgi