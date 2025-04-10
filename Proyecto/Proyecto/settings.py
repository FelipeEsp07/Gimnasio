from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-bny*9t_o2%h$9$#@0jyx&t%zo(qp%etg+$!r)pxp^g&b5&wgfh'
DEBUG = True
# settings.py
STRIPE_PUBLIC_KEY = 'pk_test_51RBEjVPSTJcjJ6jGasH32T2KEgLmDnutQMVqkjXqu7HB6yKg6byh1EGpZwizOB1n2ryyd5JAM8NtkpkMOqSEpQ9E00qIzsfDEO'
STRIPE_SECRET_KEY = 'sk_test_51RBEjVPSTJcjJ6jGSsM5UAhtBWDhNutLwilz6BArqXdUShNrjeyTK58Vb04zZE91ZbaYaZhkjT9dQgl0bCk9lYzE00Sa4Sifzs'

# Incluye el wildcard de ngrok-free.app
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.ngrok-free.app']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Apps.Aplicacion1',
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

ROOT_URLCONF = 'Proyecto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Si tus templates están en Apps/Aplicacion1/templates, Django los encontrará con APP_DIRS=True
        'DIRS': [],
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

WSGI_APPLICATION = 'Proyecto.wsgi.application'

# --- Conexión a MySQL ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gimnasio',
        'USER': 'root',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': 3306,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# --- Validadores de contraseña (opcional) ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internacionalización ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Archivos estáticos ---
STATIC_URL = '/static/'
# Si más adelante pones archivos en Apps/Aplicacion1/static/, Django los encontrará
STATICFILES_DIRS = [
    BASE_DIR / 'Apps' / 'Aplicacion1' / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # para collectstatic (producción)

# --- Archivos de usuario (media) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CSRF_TRUSTED_ORIGINS = ['https://*.ngrok-free.app']
# settings.py
WKHTMLTOPDF_CMD = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
