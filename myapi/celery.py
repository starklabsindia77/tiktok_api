from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'myapi.settings')


app = Celery('myapi')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

#app.conf.beat_schedule = {
#    'send-report-every-single-minute': {
#        'task': 'publish.tasks.send_view_count_report',
#        'schedule': crontab(minute='*/5'),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#    },
#}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))