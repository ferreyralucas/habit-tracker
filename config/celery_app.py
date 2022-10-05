# coding=utf-8
import os
from celery import Celery

from django.conf import settings

# set the default Django settings module before import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings.production")


app = Celery('django')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
