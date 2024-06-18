from time import sleep
from celery import Celery
from celery.schedules import crontab



broker_url = "amqp://guest@rabbit//"
app = Celery('tasks', broker=broker_url)

app.conf.beat_schedule = {
    'check_complered_bookings': {
        'task': 'services.celery.update_completed_bookings_status',
        'schedule': crontab(minute="*/1"),
    }
}



