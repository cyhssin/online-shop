from celery import Celery
from datetime import timedelta
import os
"""
This module configures Celery for the Django project.

- Sets the default Django settings module for the Celery program.
- Initializes a Celery application instance with the name 'core'.
- Automatically discovers tasks from all registered Django app configs.
- Configures the broker URL for RabbitMQ.
- Configures the result backend to use RPC.
- Sets the task serializer to JSON.
- Sets the result serializer to pickle.
- Accepts content types JSON and pickle.
- Sets the result expiration time to 1 day.
- Disables task eager execution.
- Sets the worker prefetch multiplier to 4.
"""

# set the default Django settings module for the celery program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.autodiscover_tasks()

app.conf.broker_url = "amqp://"
app.conf.result_backend = "rpc://"
app.conf.task_serializer = "json"
app.conf.result_serializer = "pickle"
app.conf.accept_content = ["json", "pickle"]
app.conf.result_expires = timedelta(days=1)
app.conf.task_always_eager = False
app.conf.worker_prefetch_multiplier = 4