ARG PROJECT_PATH=/freeyeti

FROM freeyeti/dev-in-docker:python3.10-gdal3.4.1 AS django

ARG PROJECT_PATH

# Set timezone
ENV TZ America/Toronto
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set LANG
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV LANGUAGE en_US:en

RUN mkdir /statics && mkdir /data && mkdir /www_data
RUN mkdir -p $PROJECT_PATH
WORKDIR $PROJECT_PATH
COPY . .

# Project initalization
ENV DJANGO_SETTINGS_MODULE "freeyeti.settings.build"

RUN poetry export --output requirements.txt \
    && yes | pip3 install --no-cache-dir -r requirements.txt \
    && python3 manage.py collectstatic --noinput \
    && pyinstaller app_all.spec

ENV DJANGO_SETTINGS_MODULE "freeyeti.settings.production"
ENV DJANGO_LOG_FILE "/data/logs/debug.log"

RUN chmod +x /app/manage/docker-entrypoint.sh
RUN chmod +x /app/manage/docker-entrypoint-migrate.sh

WORKDIR /app/manage

EXPOSE 8000
VOLUME [ "/www_data" ]
