#!/bin/sh
mkdir -p /data/cache
mkdir -p /data/logs
mkdir -p /data/attachments/image
mkdir -p /data/attachments/pdf
mkdir -p /data/pdf
mkdir -p /data/html

if [ -f "$DJANGO_LOG_FILE" ]; then
    echo "$DJANGO_LOG_FILE exists."
else 
    touch $DJANGO_LOG_FILE
    echo "$DJANGO_LOG_FILE does not exist. created"
fi

./manage runserver --noreload --no-color 0.0.0.0:8000