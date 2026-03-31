import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY="django-insecure-ex1p@mtaszq+$3@%3gvsa77#8%sv26au^)gq^9mcx063k$hz@v"

DEBUG = False

ALLOWED_HOSTS = [""]
SITE_URL = ""
CSRF_TRUSTED_ORIGINS = ""

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "orders.apps.OrdersConfig",
    "phonenumber_field",
    "widget_tweaks",
    "corsheaders",
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "washer_repair.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ],
                ),
            ],
        },
    },
]

WSGI_APPLICATION = "washer_repair.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": env.str("POSTGRES_DB", "washer_repair_db"),
#         "USER": env.str("POSTGRES_USER", "postgres"),
#         "PASSWORD": env.str("POSTGRES_PASSWORD", "postgres"),
#         "HOST": env.str("POSTGRES_HOST", "localhost"),
#         "PORT": env.int("POSTGRES_PORT", 5432),
#     },
#     "extra": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR + "db.sqlite3"},
# }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Internationalization
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static and media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Phone number settings
PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_REGION = "RU"

TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

# Email settings
EMAIL_HOST = "smtp.yandex.ru"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 465
EMAIL_USE_SSL = True

# Yandex mail settings
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

# CorsHeaders
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]
CSRF_COOKIE_SECURE = False

try:
    from .local_settings import *
except ImportError:
    pass
