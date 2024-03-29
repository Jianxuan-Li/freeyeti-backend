ARG PROJECT_PATH=/app

FROM docker.io/freeyeti/dev-in-docker:python3.11-pyinstaller5.13.0-poetry1.5.1 AS poetry

ARG PROJECT_PATH
RUN mkdir -p $PROJECT_PATH
WORKDIR $PROJECT_PATH
COPY . .

RUN poetry export --without youtube --output requirements.txt

FROM docker.io/freeyeti/dev-in-docker:python3.11-gdal3.6.2-libmagickwand AS django

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

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*
RUN yes | pip3 install --no-cache-dir -r requirements.txt \
    && yes | pip3 install 'git+https://github.com/ytdl-org/youtube-dl.git' \
    && yes | pip3 install --upgrade --force-reinstall 'git+https://github.com/ytdl-org/youtube-dl.git' \
    && python3 manage.py collectstatic --noinput

ENV DJANGO_SETTINGS_MODULE "app.settings.production"

COPY ./docker/docker-entrypoint-migrate ./
COPY ./docker/docker-entrypoint ./
COPY ./docker/test-in-container.sh ./

RUN chmod +x ./docker-entrypoint
RUN chmod +x ./docker-entrypoint-migrate
RUN chmod +x ./test-in-container.sh

EXPOSE 8000
VOLUME [ "/www_data" ]

CMD [ "./docker-entrypoint" ]
