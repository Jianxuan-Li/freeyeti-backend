from .base import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

try:
    from .local import *
except ImportError:
    pass
