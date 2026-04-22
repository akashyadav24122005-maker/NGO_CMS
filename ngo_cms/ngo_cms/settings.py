# ngo_cms/settings.py  (Modified + Clean Final Version)

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


# ===============================
# SECURITY
# ===============================
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-local-key"
)

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "AkashYadav2412.pythonanywhere.com",
]


# ===============================
# RAZORPAY KEYS
# ===============================
RAZORPAY_KEY_ID = os.environ.get(
    "RAZORPAY_KEY_ID",
    "rzp_test_SgACHtj3nDuztw"
)

RAZORPAY_KEY_SECRET = os.environ.get(
    "RAZORPAY_KEY_SECRET",
    "vxTm0GcTmXMNYHzplZ47ilVR"
)


# ===============================
# INSTALLED APPS
# ===============================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "core",
]


# ===============================
# MIDDLEWARE
# ===============================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "ngo_cms.urls"
WSGI_APPLICATION = "ngo_cms.wsgi.application"


# ===============================
# TEMPLATES
# ===============================
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


# ===============================
# DATABASE
# ===============================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ===============================
# PASSWORD VALIDATORS
# ===============================
AUTH_PASSWORD_VALIDATORS = []


# ===============================
# LANGUAGE / TIME
# ===============================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


# ===============================
# STATIC FILES
# ===============================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)


# ===============================
# MEDIA FILES
# ===============================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ===============================
# DEFAULT PRIMARY KEY
# ===============================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ===============================
# LOGIN / LOGOUT
# ===============================
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"


# ===============================
# EMAIL
# ===============================
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"