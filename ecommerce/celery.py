import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")

# set the default Django settings module for the 'celery' program.
app = Celery("ecommerce", broker="amqp://guest@localhost//")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()