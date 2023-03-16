ARG PROJECT_PATH=/app

FROM docker.io/freeyeti/dev-in-docker:pyinstaller5.8.0-poetry1.4.0 AS poetry

ARG PROJECT_PATH
RUN mkdir -p $PROJECT_PATH
WORKDIR $PROJECT_PATH
COPY . .

RUN poetry export --output requirements.txt

FROM docker.io/freeyeti/dev-in-docker:python3.10-gdal3.4.1-libmagickwand AS django

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

COPY --from=poetry /$PROJECT_PATH/requirements.txt ./

# Project initalization
ENV DJANGO_SETTINGS_MODULE "app.settings.build"

RUN yes | pip3 install --no-cache-dir -r requirements.txt \
    && python3 manage.py collectstatic --noinput

ENV DJANGO_SETTINGS_MODULE "app.settings.production"

COPY ./docker/docker-entrypoint-migrate ./
COPY ./docker/docker-entrypoint ./
COPY ./docker/test-in-container.sh ./
COPY ./docker/backup-db.sh ./

RUN chmod +x ./docker-entrypoint
RUN chmod +x ./docker-entrypoint-migrate
RUN chmod +x ./test-in-container.sh
RUN chmod +x ./backup-db.sh

EXPOSE 8000
VOLUME [ "/www_data" ]

CMD [ "./docker-entrypoint" ]
