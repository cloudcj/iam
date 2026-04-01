from pathlib import Path
from datetime import timedelta
import environ
import os
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# --------------------------------------------------
# Core
# --------------------------------------------------
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# --------------------------------------------------
# Applications
# --------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',

    # Apps
    'inventory.infrastructure',
    'inventory.assets',
    'inventory.enums',
    'inventory.logs',
    'inventory.common',
  
    # IAM integration
    'iam',
]

# --------------------------------------------------
# Middleware
# --------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'inventory.logs.middleware.AccessLogMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --------------------------------------------------
# Database
# --------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DATABASE_NAME"),
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST': env("DATABASE_HOST"),
        'PORT': env("DATABASE_PORT"),
    }
}

# --------------------------------------------------
# Cache (Redis)
# --------------------------------------------------
REDIS_HOST = env("REDIS_HOST")
REDIS_PORT = env("REDIS_PORT")
REDIS_DB = env("REDIS_DB")
REDIS_PASSWORD = env("REDIS_PASSWORD", default="")

REDIS_URL = f"redis://{':' + REDIS_PASSWORD + '@' if REDIS_PASSWORD else ''}{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}

# --------------------------------------------------
# JWT / IAM Integration (disabled — IAM to be built separately)
# --------------------------------------------------
IAM_PUBLIC_KEY_PATH = env("IAM_PUBLIC_KEY_PATH", default="")

if IAM_PUBLIC_KEY_PATH and Path(IAM_PUBLIC_KEY_PATH).exists():
    SIMPLE_JWT = {
        "ALGORITHM": "RS256",
        "SIGNING_KEY": None,
        "VERIFYING_KEY": Path(IAM_PUBLIC_KEY_PATH).read_text(),
        "ISSUER": env("IAM_ISSUER", default="gaia-iam"),
        "AUDIENCE": env("IAM_AUDIENCE", default="gaia-api"),
        "AUTH_HEADER_TYPES": ("Bearer",),
        "USER_ID_FIELD": "id",
        "USER_ID_CLAIM": "sub",
        "AUTH_TOKEN_CLASSES": (
            "rest_framework_simplejwt.tokens.AccessToken",
        ),
    }

# --------------------------------------------------
# Django REST Framework
# --------------------------------------------------
REST_FRAMEWORK = {
    # AUTHENTICATION
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'iam.authentication.IAMAuthentication',
    ],

    # AUTHORIZATION
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_PAGINATION_CLASS': 'inventory.common.pagination.CustomPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],

    'EXCEPTION_HANDLER': 'inventory.common.exceptions.custom_exception_handler',
}

# --------------------------------------------------
# Auth
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --------------------------------------------------
# CORS / CSRF
# --------------------------------------------------
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = "Lax"

SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = "Lax"

# --------------------------------------------------
# Internationalization
# --------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

# --------------------------------------------------
# Static / Media
# --------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "inventory" / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
