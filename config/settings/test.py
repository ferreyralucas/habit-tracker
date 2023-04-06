from .base import *  # noqa
from .base import env

DATABASES = {"default": env.db("DATABASE_URL")}

# GENERAL
DEBUG = True
TEST_RUNNER = "django.test.runner.DiscoverRunner"


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": ""
    }
}
