"""
Django settings for crawler project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from .config import SERVER_CONFIG, EMAIL_BACKEND_CONFIG
from module.date import DateTimeTools as DT


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SERVER_CONFIG.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = SERVER_CONFIG.ALLOWED_HOSTS

CORS_ORIGIN_ALLOW_ALL = SERVER_CONFIG.CORS_ORIGIN_SETTING['ALLOW_ALL']

CORS_ORIGIN_WHITELIST = SERVER_CONFIG.CORS_ORIGIN_WHITELIST

# CORS_ORIGIN_REGEX_WHITELIST = SERVER_CONFIG.CORS_ORIGIN_REGEX_WHITELIST

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'stock',
    'tasks',
    'ptt',
    'google_search',
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'crawler.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'crawler.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Crawler',
        'USER': SERVER_CONFIG.MARIADB_SETTING['username'],
        'PASSWORD': SERVER_CONFIG.MARIADB_SETTING['password'],
        'HOST': SERVER_CONFIG.MARIADB_SETTING['host'][1],
        'PORT': SERVER_CONFIG.MARIADB_SETTING['port'],
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}

# Django Redis Setting
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{SERVER_CONFIG.REDIS_SETTING['host'][-1]}:{SERVER_CONFIG.REDIS_SETTING['port']}/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# MEDIA_URL = 'media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# DATABASE_ROUTERS = ['routers.db_routers.AuthRouter']

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.JWTAuthentication',
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': DT.obtain_minutes_datetime(SERVER_CONFIG.JWT_TOKEN_SETTING['ACCESS_TOKEN_LIFETIME']),
    'REFRESH_TOKEN_LIFETIME': DT.obtain_days_datetime(SERVER_CONFIG.JWT_TOKEN_SETTING['REFRESH_TOKEN_LIFETIME']),
    'SIGNING_KEY': SECRET_KEY,
    # 'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'UPDATE_LAST_LOGIN': SERVER_CONFIG.JWT_TOKEN_SETTING['UPDATE_LAST_LOGIN'],
}

AUTHENTICATION_BACKENDS = [
    'users.backends.ModelBackend',
]

SERVER_BASE_URL = SERVER_CONFIG.SERVER_BASE_URL[0]

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = f"amqp://{SERVER_CONFIG.RABBITMQ_SETTING['username']}:{SERVER_CONFIG.RABBITMQ_SETTING['password']}@{SERVER_CONFIG.RABBITMQ_SETTING['host'][-1]}:{SERVER_CONFIG.RABBITMQ_SETTING['port']}/{SERVER_CONFIG.RABBITMQ_SETTING['vhost']}"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# SMTP Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = EMAIL_BACKEND_CONFIG.SMTP_HOST
EMAIL_PORT = EMAIL_BACKEND_CONFIG.SMTP_PORT
EMAIL_USE_TLS = EMAIL_BACKEND_CONFIG.EMAIL_USE_TLS
EMAIL_HOST_USER = EMAIL_BACKEND_CONFIG.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_BACKEND_CONFIG.EMAIL_HOST_PASSWORD

SILENCED_SYSTEM_CHECKS = ['mysql.E001']