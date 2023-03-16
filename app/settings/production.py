from .base import *

DEBUG = False

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "formatter": "verbose",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": True,
        },
    },
}

# allowed hosts
ALLOWED_HOSTS = ["freeyeti.net", "www.freeyeti.net"]

FORCE_SCRIPT_NAME = "/backend"
STATIC_URL = "/backend/static/"
MEDIA_URL = "/backend/media/"

CSRF_TRUSTED_ORIGINS = [
    "https://freeyeti.net",
    "https://www.freeyeti.net",
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# database optimized for production
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PWD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "TEST": {"NAME": os.environ.get("TEST_DB_NAME")},
        "CONN_MAX_AGE": 60,
        "CONN_HEALTH_CHECKS": True,
    }
}

try:
    from .local import *
except ImportError:
    pass
