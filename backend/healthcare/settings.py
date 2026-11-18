import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "development-only-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "true").lower() == "true"
ALLOWED_HOSTS = [host for host in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if host]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "tenants",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "tenants.middleware.TenantMiddleware",
]

ROOT_URLCONF = "healthcare.urls"
WSGI_APPLICATION = "healthcare.wsgi.application"

if os.getenv("POSTGRES_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("CENTRAL_DB_NAME", "central"),
            "USER": os.getenv("POSTGRES_USER", "healthcare"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "healthcare"),
            "HOST": os.getenv("POSTGRES_HOST"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        },
        "tenant_a": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("TENANT_A_DB_NAME", "tenant_a"),
            "USER": os.getenv("POSTGRES_USER", "healthcare"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "healthcare"),
            "HOST": os.getenv("TENANT_A_DB_HOST", os.getenv("POSTGRES_HOST")),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        },
        "tenant_b": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("TENANT_B_DB_NAME", "tenant_b"),
            "USER": os.getenv("POSTGRES_USER", "healthcare"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "healthcare"),
            "HOST": os.getenv("TENANT_B_DB_HOST", os.getenv("POSTGRES_HOST")),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        },
    }
else:
    DATABASES = {
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "central.sqlite3"},
        "tenant_a": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "tenant_a.sqlite3"},
        "tenant_b": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "tenant_b.sqlite3"},
    }

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = ["accept", "authorization", "content-type", "x-tenant"]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
}

TENANT_DATABASES = {
    "tenant-a": "tenant_a",
    "tenant-b": "tenant_b",
}
