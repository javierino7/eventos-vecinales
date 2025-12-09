from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "REEMPLAZA-ESTE-SECRET-KEY-EN-PROD"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps del proyecto (orden importa)
    "accounts",
    "events",
]

AUTH_USER_MODEL = "accounts.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "eventos_vecinales.urls"
WSGI_APPLICATION = "eventos_vecinales.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # /templates a nivel proyecto
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "eventos_db_clean",            # <-- cambia si usaste otro
        "USER": "administrador",               # si es necesario en Azure: "administrador@ev-mysql-vecinal"
        "PASSWORD": "Javieramigo11@",        # <-- tu pass real aquí
        "HOST": "ev-mysql-vecinal.mysql.database.azure.com",
        "PORT": "3306",
        "OPTIONS": {"ssl": {"ssl_mode": "REQUIRED"}},
        "CONN_MAX_AGE": 60,
    }
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@eventos-vecinales.local"

LOGIN_URL = "login"                 # /accounts/login/
LOGIN_REDIRECT_URL = "events:listar"
LOGOUT_REDIRECT_URL = "login"

LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
# STATIC_ROOT = BASE_DIR / "staticfiles"  # para prod

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


from pathlib import Path
import os

# ... tu configuración que ya tienes arriba ...

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


LOGIN_REDIRECT_URL = "events:listar"
LOGIN_URL = "accounts:login"
LOGOUT_REDIRECT_URL = "accounts:login"



from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'



# settings.py

# A dónde te manda cuando NO estás logueado
LOGIN_URL = "login"  # <- antes estaba 'accounts:login'

# A dónde te manda después de cerrar sesión
LOGOUT_REDIRECT_URL = "login"  # <- antes estaba 'accounts:login'

# A dónde te manda después de iniciar sesión OK
LOGIN_REDIRECT_URL = "events:listar"