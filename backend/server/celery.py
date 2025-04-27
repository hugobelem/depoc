import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')

app.conf.broker_connection_retry_on_startup = True
app.conf.beat_schedule = {
    'update-payments-daily': {
        'task': 'modules.billing.tasks.update_payment_status',
        'schedule': 10.0,
    }
}

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
