import os

import random

import requests

from celery import shared_task

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from django.db import transaction
from django.db.models import F
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from src.fruit_shop.models import (
    Message,
    Fruit,
    Trade,
    Balance
)


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


@transaction.atomic
def trade_fruits(action, fruit_type, quantity=None):
    channel_layer = get_channel_layer()

    balance = Balance.objects.select_for_update().first()
    fruit = Fruit.objects.select_for_update().get(name=fruit_type)

    if not quantity:
        quantity = random.randint(*fruit.get_range(action))

    price = fruit.buy_price if action == Trade.Action.BUY else fruit.sell_price
    total_price = quantity * price

    success = False

    if action == Trade.Action.BUY:
        if balance.value >= total_price:
            balance.value = F("value") - total_price
            fruit.quantity = F("quantity") + quantity
            success = True
    else:
        if fruit.quantity >= quantity:
            balance.value = F("value") + total_price
            fruit.quantity = F("quantity") - quantity
            success = True

    if success:
        balance.save()
        fruit.save()
        balance.refresh_from_db()
        fruit.refresh_from_db()

    trade = Trade.objects.create(
        action=action,
        fruit=fruit,
        quantity=quantity,
        status=Trade.Status.SUCCESS if success else Trade.Status.ERROR
    )

    def send_ws_events():
        async_to_sync(channel_layer.group_send)(
            "balance",
            {
                "type": "balance_update",
                "balance": balance.value,
            }
        )
        async_to_sync(channel_layer.group_send)(
            "trade",
            {
                "type": "trade_log",
                "id": trade.id,
            }
        )

    transaction.on_commit(send_ws_events)


@shared_task(name="buy_apples", queue="warehouse")
def buy_apples(): trade_fruits("Buy", Fruit.Type.APPLE)


@shared_task(name="buy_bananas", queue="warehouse")
def buy_bananas(): trade_fruits("Buy", Fruit.Type.BANANA)


@shared_task(name="buy_pineapples", queue="warehouse")
def buy_pineapples(): trade_fruits("Buy", Fruit.Type.PINEAPPLE)


@shared_task(name="buy_peaches", queue="warehouse")
def buy_peaches(): trade_fruits("Buy", Fruit.Type.PEACH)


@shared_task(name="sell_apples", queue="warehouse")
def sell_apples(): trade_fruits("Sell", Fruit.Type.APPLE)


@shared_task(name="sell_bananas", queue="warehouse")
def sell_bananas(): trade_fruits("Sell", Fruit.Type.BANANA)


@shared_task(name="sell_pineapples", queue="warehouse")
def sell_pineapples(): trade_fruits("Sell", Fruit.Type.PINEAPPLE)


@shared_task(name="sell_peaches", queue="warehouse")
def sell_peaches(): trade_fruits("Sell", Fruit.Type.PEACH)


@shared_task(name="trade_fruit", queue="warehouse")
def trade_fruit(action, fruit_type, quantity):
    trade_fruits(action, fruit_type, quantity)


@shared_task(name="update_balance", queue="balance")
def update_balance(action: str, amount: int):
    channel_layer = get_channel_layer()

    with transaction.atomic():
        balance = Balance.objects.select_for_update().first()

        if action == "Replenish":
            balance.value = F("value") + amount
        elif action == "Withdraw":
            balance.value = F("value") - amount

        balance.save()
        balance.refresh_from_db()

        transaction.on_commit(lambda: async_to_sync(channel_layer.group_send)(
            "balance",
            {
                "type": "balance_update",
                "balance": balance.value,
            }
        ))
