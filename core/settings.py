from pathlib import Path
import os
import dj_database_url
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x-99b4kh&n@yepyojeh#u9%)yib$l2zm%aop8*txwtew6dp6qh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

CSRF_TRUSTED_ORIGINS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'channels',
    'rest_framework',
    'corsheaders',
    'Products.apps.ProductsConfig',
    'drf_spectacular',
    
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'frontend' / 'templates' ],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError('⚠️ Defina DATABASE_URL no .env')

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL),
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Celery Configuration Options
LANGUAGE_CODE = 'pt-br'

# Puxa do .env (definidos nos services celery_worker e celery_beat)
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
CELERY_TIMEZONE = 'America/Sao_Paulo'
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"



# (opcional) serialize formatos
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CORS_ALLOW_ORIGINS = [
    'http://127.0.0.1:2025/',
    'http://localhost:2025/',
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Onde o collectstatic vai colocar os arquivos empacotados
STATIC_ROOT = BASE_DIR / 'staticfiles'

# URL pra servir estáticos
STATIC_URL = '/static/'

# Opcional: compactar e gerar hash nos arquivos pra cache
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ENV = os.getenv("ENV", "development")  # valor padrão é "development"

if ENV == "production":
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://redis:6379/0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
else:
    # Cache local para desenvolvimento (sem latência)
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "dev-cache",
        }
    }
    
# Channels: sempre use RedisChannelLayer, indiferente do ENV
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # ajuste a URL se você tiver senha ou porta diferente
            "hosts": [os.getenv("REDIS_URL", "redis://redis:6379/1")],
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'PDD Management API Rest',
    'DESCRIPTION': 'API Rest personalizada totalmente para o funcionamento da aplicação',
    'VERSION': '0.0.1',
    'SERVE_INCLUDE_SCHEMA': True,
    'SCHEMA_PATH_PREFIX_TRIM': None,
    'COMPONENT_SPLIT_REQUEST': True,
    'OAS_VERSION': '3.1.0',
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "channels_redis": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
}

# CELERY_BEAT_SCHEDULE = {
#     # Task para capturar o skuId de todos os produtos na VTEX - roda a cada 10 minutos
#     "get_list_sku_ids": {
#         "task": "Products.tasks.get_list_sku_ids",
#         "schedule": 600.0,  # em segundos
       
#     },
#     # Task para capturar da VTEX o contexto dos produtos peli skuId - roda a cada 15 minutos
#     "get_sku_context_by_sku_id": {
#         "task": "Products.tasks.get_sku_context_by_sku_id",
#         "schedule": 900.0,  # em segundos
#     },
# }