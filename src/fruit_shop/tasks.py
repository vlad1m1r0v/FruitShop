import os

import requests

from celery import shared_task

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from django.template.loader import render_to_string
from django.contrib.auth.models import User

from src.fruit_shop.models import Message


@shared_task(name="send_joke", queue="jokes")
def send_joke():
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    joke_data = response.json()

    content = f"\n-🤔 {joke_data['setup']}\n-😀 {joke_data['punchline']}"

    joker = User.objects.get(username="Joker🤡")

    created_message = Message.objects.create(author=joker, content=content)

    new_message = Message.objects.select_related('author').get(pk=created_message.id)

    channel_layer = get_channel_layer()
    message_html = render_to_string(
        template_name='partials/messages_list.html',
        context={'messages': [new_message]}
    )

    async_to_sync(channel_layer.group_send)(
        'chat',
        {
            'type': 'chat_message',
            'html': message_html
        }
    )

    countdown = len(content)

    send_joke.apply_async(countdown=countdown, queue="jokes")


@shared_task(name="financial_audit", queue="audit")
def financial_audit():
    channel_layer = get_channel_layer()

    for i in range(50):
        chunk = os.urandom(1024 * 1024 * 96)

        progress = i * 2

        async_to_sync(channel_layer.group_send)(
            "audit",
            {"type": "progress_update", "progress": progress}
        )

        del chunk

    async_to_sync(channel_layer.group_send)(
        "audit",
        {
            "type": "progress_update",
            "progress": 100,
        }
    )
