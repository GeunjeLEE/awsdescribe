import os 
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pj_awsdescribe.settings')

app = Celery('pj_awsdescribe')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'every-day-5am-a': {
        'task': 'sync_part_a',
        'schedule': crontab(minute=50, hour=4)
    },
    'every-day-5am-b': {
        'task': 'sync_part_b',
        'schedule': crontab(minute=00, hour=5)
    },
    'every-day-5am-c': {
        'task': 'sync_part_c',
        'schedule': crontab(minute=10, hour=5)
    },
}