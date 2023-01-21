ARG PROJECT_PATH=/website

FROM freeyeti/dev-in-docker:pyinstaller5.7.0-poetry1.3.1 AS backend

ARG PROJECT_PATH

RUN mkdir /statics && mkdir /data && mkdir /www_data
RUN mkdir -p $PROJECT_PATH
WORKDIR $PROJECT_PATH
COPY . .

# Create working dir

# Project initalization
ENV DJANGO_SETTINGS_MODULE "app.settings_build"

COPY ./pyi_rth_django.py /usr/local/lib/python3.10/dist-packages/PyInstaller/hooks/rthooks/pyi_rth_django.py

RUN poetry export --output requirements.txt \
    && yes | pip3 install --no-cache-dir -r requirements.txt \
    && python3 manage.py collectstatic --noinput \
    && pyinstaller app_all.spec

FROM freeyeti/dev-in-docker:python3.10-gdal3.4.1 AS django

# Set timezone
ENV TZ America/Toronto
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set LANG
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV LANGUAGE en_US:en

ARG PROJECT_PATH

ENV DJANGO_SETTINGS_MODULE "app.settings"
ENV DJANGO_LOG_FILE "/data/logs/debug.log"

COPY --from=backend /$PROJECT_PATH/dist /app
COPY --from=backend /$PROJECT_PATH/docker-entrypoint-migrate.sh /app/manage/docker-entrypoint-migrate.sh
COPY --from=backend /$PROJECT_PATH/docker-entrypoint.sh /app/manage/docker-entrypoint.sh
COPY --from=backend /$PROJECT_PATH/ /app/manage/
COPY --from=backend /statics /statics
RUN chmod +x /app/manage/docker-entrypoint.sh
RUN chmod +x /app/manage/docker-entrypoint-migrate.sh

WORKDIR /app/manage

EXPOSE 8000
VOLUME [ "/www_data" ]
