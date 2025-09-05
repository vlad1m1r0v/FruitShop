import os
from celery import Celery
from kombu import Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.conf.broker_url = os.getenv("CELERY_BROKER_URL")
app.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")

app.conf.task_default_queue = "default"
app.conf.task_queues = (
    Queue("trade", routing_key="trade"),
    Queue("warehouse", routing_key="warehouse"),
    Queue("jokes", routing_key="jokes"),
    Queue("audit", routing_key="audit"),
    Queue("balance", routing_key="balance"),
)

app.conf.beat_schedule = {
    "buy_apples": {"task": "buy_apples", "schedule": 6.0},
    "buy_bananas": {"task": "buy_bananas", "schedule": 9.0},
    "buy_pineapples": {"task": "buy_pineapples", "schedule": 12.0},
    "buy_peaches": {"task": "buy_peaches", "schedule": 15.0},
    "sell_apples": {"task": "sell_apples", "schedule": 15.0},
    "sell_bananas": {"task": "sell_bananas", "schedule": 12.0},
    "sell_pineapples": {"task": "sell_pineapples", "schedule": 9.0},
    "sell_peaches": {"task": "sell_peaches", "schedule": 6.0},
}

app.autodiscover_tasks()