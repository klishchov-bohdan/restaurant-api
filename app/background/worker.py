from celery import Celery

from app.config import settings

__BROKER_URL = f'pyamqp://{settings.rabbitmq.default_user}:{settings.rabbitmq.default_password}@' \
    f'{settings.rabbitmq.host}:{settings.rabbitmq.port}//'

worker = Celery(
    'celery_api',
    broker=__BROKER_URL,
    backend='rpc://',
    include=['app.background.tasks']
)
