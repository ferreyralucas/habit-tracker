import sys

import django
from django.utils.encoding import force_str, smart_str

import environ
from kombu import Exchange, Queue

"""
TEMPORAL FIX POR DJANGO > 4.0
THERE IS AN ERROR RUNNING THE COLLECTION STATIC PIPELINE BECAUSE IT GIVES THE FOLLOWING ERRORS
ImportError: cannot import name 'force_text' from 'django.utils.encoding'
ImportError: cannot import name 'smart_text' from 'django.utils.encoding'
IN DJANGO 4 THE FORCE_TEXT AND SMART_TEXT METHOD WERE REMOVED
https://docs.djangoproject.com/en/4.0/releases/4.0/#features-removed-in-4-0
THE PROBLEM IS THAT THERE ARE LIBRARIES THAT STILL USE THOSE METHODS SO WE HAVE TO ADD THIS FIX
"""
# ------------------- START OF FIX
django.utils.encoding.force_text = force_str
django.utils.encoding.smart_text = smart_str
# ------------------- END OF FIX


ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('apps')

env = environ.Env()

ENVIRONMENT = env('ENVIRONMENT')

env.read_env(str(ROOT_DIR.path('.env')))

if ENVIRONMENT == 'test':
    env.read_env(str(ROOT_DIR.path('env.test')))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, ROOT_DIR('apps'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')


ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", [])
CSRF_TRUSTED_ORIGINS = ['https://*']


# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'django_filters'
]

LOCAL_APPS = [
    'tax_payers'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'easy_health_check.middleware.HealthCheckMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'config.wsgi.application'


# # DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL')
}


# # PASSWORD VALIDATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
    },
]


# # INTERNATIONALIZATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Buenos_Aires'
USE_I18N = True
USE_TZ = True


# # STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = str(ROOT_DIR("staticfiles"))
STATIC_URL = '/static/'
STATICFILES_DIRS = []

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# # MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = str(ROOT_DIR('media'))
MEDIA_URL = '/media/'


# # DJANGO REST FRAMEWORK
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}


# # CORS APP
# ------------------------------------------------------------------------------
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True


# # REDIS
# ------------------------------------------------------------------------------
REDIS_LOCK_URL = env.str('REDIS_URL')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str('REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# # CELERY CONFIGS
# ------------------------------------------------------------------------------
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env.str('REDIS_URL')
CELERY_MAX_CACHED_RESULTS = 1000
CELERY_TASK_RESULT_EXPIRES = env.int('CELERY_TASK_RESULT_EXPIRES', 10000)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

default_exchange = Exchange("default", type="direct")
DEFAULT_QUEUE = "default"

CELERY_TASK_QUEUES = (
    Queue(DEFAULT_QUEUE, default_exchange, routing_key=DEFAULT_QUEUE)
)

CELERY_ROUTES = {
    # 'some.task.*': {
    #     'queue': DEFAULT_QUEUE,
    #     'routing_key': DEFAULT_QUEUE,
    # }
}

CELERY_TASK_DEFAULT_QUEUE = DEFAULT_QUEUE
CELERY_TASK_DEFAULT_EXCHANGE = DEFAULT_QUEUE
CELERY_TASK_DEFAULT_ROUTING_KEY = DEFAULT_QUEUE


# # SENTRY
# ------------------------------------------------------------------------------
SENTRY_DSN = env('SENTRY_DSN', default=None)
if SENTRY_DSN:
    import sentry_sdk

    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), CeleryIntegration()],
        environment=ENVIRONMENT,
    )


# # AWS S3 CONFIGS
# ------------------------------------------------------------------------------
if env("AWS_ACCESS_KEY_ID", default=""):
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")


# # MIDDLEWARE https://pypi.org/project/django-easy-health-check/
# ------------------------------------------------------------------------------
DJANGO_EASY_HEALTH_CHECK = {
    "PATH": "/healthcheck/",
    "RETURN_STATUS_CODE": 200,
    "RETURN_BYTE_DATA": "",
    "RETURN_HEADERS": None
}
