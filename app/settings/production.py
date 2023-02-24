from .base import *

DEBUG = False

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'formatter': 'verbose',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.environ.get('DJANGO_LOG_FILE'),
            'when': 'midnight',
            'interval': 1
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# allowed hosts
ALLOWED_HOSTS = ['freeyeti.net', 'www.freeyeti.net']

FORCE_SCRIPT_NAME = "/backend"

CSRF_TRUSTED_ORIGINS = [
    'https://freeyeti.net',
    'https://www.freeyeti.net',
]

try:
    from .local import *
except ImportError:
    pass
