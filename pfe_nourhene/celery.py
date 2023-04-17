import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pfe_nourhene.settings')

app = Celery('pfe_nourhene')
app.conf.broker_connection_timeout = 30
app.conf.broker_connection_retry = True
app.conf.broker_connection_max_retries = 3
app.conf.task_acks_late = True
app.conf.worker_prefetch_multiplier = 1

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


