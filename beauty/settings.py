import os
from pathlib import Path

# Path to firebase service account JSON or raw JSON string
FIREBASE_ADMIN_CREDENTIAL = os.getenv('FIREBASE_ADMIN_CREDENTIAL')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'replace-me-with-secure-key'
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

# Django will reject requests when DEBUG=False unless the host is allowed
# (commonly `testserver` during `manage.py test`). Environment variable provides
# production hosts; if it's empty we still need to permit the test server and
# localhost so the built‑in test client works.
allowed = os.getenv('DJANGO_ALLOWED_HOSTS', '')
ALLOWED_HOSTS = allowed.split(',') if allowed else []
if not ALLOWED_HOSTS:
    # minimal defaults for development/testing; production deployments should set
    # DJANGO_ALLOWED_HOSTS explicitly via env var.
    ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'channels',
    'users',
    'experts',
    'appointments',
    'reviews',
    'chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'beauty.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'beauty.wsgi.application'
ASGI_APPLICATION = 'beauty.asgi.application'

import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# Directory where `collectstatic` will copy files for production
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'utils.drf_firebase_auth.FirebaseAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'EXCEPTION_HANDLER': 'utils.drf_exception_handler.custom_exception_handler',
}
# allow firebase backend alongside default
AUTHENTICATION_BACKENDS = [
    'users.auth_backends.FirebaseBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Pagination
REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'] = 'rest_framework.pagination.PageNumberPagination'
REST_FRAMEWORK['PAGE_SIZE'] = 12

# Channels in-memory layer for development
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# Production-level security settings (enabled when DEBUG=False).
# These are turned off during testing (both with manage.py test and pytest)
# so that the test client doesn't get redirected to https and ALLOWED_HOSTS
# doesn't block the requests.
if not DEBUG and os.getenv('PYTEST_CURRENT_TEST') is None and 'test' not in __import__('sys').argv:
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)
    if SECRET_KEY == 'replace-me-with-secure-key':
        raise ValueError('DJANGO_SECRET_KEY must be set in production')
    
    # HTTPS / SSL settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS settings (be careful: only enable if you're sure about HTTPS everywhere)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Other security headers
    SECURE_CONTENT_SECURITY_POLICY = {
        'default-src': ("'self'",),
        'script-src': ("'self'", "'unsafe-inline'", "https://apis.google.com"),
        'connect-src': ("'self'", "https://identitytoolkit.googleapis.com"),
        'img-src': ("'self'", "data:", "https:"),
        'font-src': ("'self'",),
        'frame-ancestors': ("'none'",),
    }
    
    # Allow iframe for Firebase only if needed
    X_FRAME_OPTIONS = 'DENY'
