import os

from celery import Celery
from django.conf import settings as django_settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

app = Celery(django_settings.CELERY_APP_NAME)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
