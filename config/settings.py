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

AUTH_USER_MODEL = 'accounts.CustomUser'

SITE_ID = 3

ALLOWED_HOSTS = (
    ["*"]
    if DEBUG
    else config(
        "ALLOWED_HOSTS", cast=lambda host: [h.strip() for h in host.split(",") if h]
    )
)


APPLICATIONS = ["accounts", "order", "shop"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.sites',

    # third-party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',

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
    "allauth.account.middleware.AccountMiddleware",
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

AUTHENTICATION_BACKENDS = (
    "apps.accounts.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Django Allauth config
SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "VERIFIED_EMAIL": True,
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    },
    "google": {
        "APPS": [
            {
                "client_id": config("GOOGLE_CLIENT_ID"),
                "secret": config("GOOGLE_CLIENT_SECRET"),
                "key": config("GOOGLE_CLIENT_KEY")
            },
        ],
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        'FETCH_USERINFO': True
    }
}

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

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

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = "0djangoonlineshop0@gmail.com"
    # EMAIL_HOST_PASSWORD = "1h+7L$<d1H49"  # Gmail Password
    EMAIL_HOST_PASSWORD = "tmvhfhllyqztbhex"

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
