from time import sleep
from celery import Celery

broker_url = "amqp://guest@rabbit//"
app = Celery('tasks', broker=broker_url)

@app.task
def say_hello(name: str):
    sleep(5)
    return f"Hello {name}"

