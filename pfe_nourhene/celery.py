import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pfe_nourhene.settings')

app = Celery('pfe_nourhene')
app.conf.broker_connection_timeout = 30
app.conf.broker_connection_retry = True
app.conf.broker_connection_max_retries = 3
app.conf.task_acks_late = True
app.conf.worker_prefetch_multiplier = 1


app.config_from_object('django.conf:settings', namespace='CELERY')


worker_cancel_long_running_tasks_on_connection_loss = True

acks_late=True
app.autodiscover_tasks()


