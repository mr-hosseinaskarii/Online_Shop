from pathlib import Path
from decouple import config

LANGUAGE_CODE = "en-us"

USE_I18N = True

USE_TZ = True

WSGI_APPLICATION = "config.wsgi.application"

BASE_DIR = Path(__file__).resolve().parent.parent

APP_DIR = BASE_DIR / "apps"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "config.urls"

SECRET_KEY = config("SECRET_KEY", default="secret-key-!!!")

DEBUG = config("DEBUG", cast=bool, default=True)

TIME_ZONE = config("TIME_ZONE", default="UTC")

ALLOWED_HOSTS = (
    ["*"]
    if DEBUG
    else config(
        "ALLOWED_HOSTS", cast=lambda host: [h.strip() for h in host.split(",") if h]
    )
)


APPLICATIONS = ["account", "order", "shop"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # third-party

    # custom apps
    *list(map(lambda app: f"apps.{app}", APPLICATIONS))
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


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


# Serving
STATIC_URL = "static/"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "storage/media"


# Mode Handling:
if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / "storage/static"]

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": BASE_DIR / "tmp/cache",
        }
    }

    EMAIL_USE_TLS = False
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 25
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    DEFAULT_FROM_EMAIL = "noreply@maktab105.dev"

else:
    REDIS_URL = f"redis://{config('REDIS_HOST')}:{config('REDIS_PORT')}"

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST"),
            "PORT": config("DB_PORT"),
        }
    }

    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        }
    }

    EMAIL_USE_TLS = config("EMAIL_USE_TLS")
    EMAIL_USE_SSL = config("EMAIL_USE_SSL")
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_PORT = config("EMAIL_PORT")
    EMAIL_HOST_USER = config("EMAIL_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
    DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
