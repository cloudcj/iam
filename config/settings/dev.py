"""
Development settings.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Dev-only convenience