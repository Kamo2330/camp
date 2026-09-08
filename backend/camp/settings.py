"""
Django settings for camp project.
"""

import os
import socket
import sys
import urllib.parse
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-only-change-in-production')
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    if host.strip()
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'camp.urls'

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

WSGI_APPLICATION = 'camp.wsgi.application'


def _local_postgres_is_up(database_url: str) -> bool:
    parsed = urllib.parse.urlparse(database_url)
    host = parsed.hostname or 'localhost'
    port = parsed.port or 5432
    if host.lower() not in ('localhost', '127.0.0.1', '::1'):
        return True
    try:
        with socket.create_connection((host, int(port)), timeout=0.4):
            return True
    except OSError:
        return False


if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    database_url = os.environ.get('DATABASE_URL', 'postgres://camp:camp@localhost:5433/camp')
    production = os.environ.get('RENDER') or not DEBUG
    if production or _local_postgres_is_up(database_url):
        DATABASES = {
            'default': dj_database_url.parse(database_url, conn_max_age=600),
        }
    else:
        print(
            'Local PostgreSQL is not running. Using SQLite so you can test '
            'without Docker. (Optional later: docker compose up -d)'
        )
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
    if origin.strip()
]

CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', 'info@campsecurity.com')
SALES_EMAIL = os.environ.get('SALES_EMAIL', 'sales@campsecurity.com')
CAREERS_EMAIL = os.environ.get('CAREERS_EMAIL', 'careers@campsecurity.com')
