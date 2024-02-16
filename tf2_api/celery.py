# tf2_api/celery.py

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tf2_api.settings")
app = Celery("tf2_api")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()