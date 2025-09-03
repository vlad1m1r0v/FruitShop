import os

import random

from django.conf import settings
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from src.fruit_shop.models import (
    Message,
    Fruit,
    Balance,
    Declaration,
    Trade,
)


def create_fruits() -> list[Fruit]:
    Fruit.objects.all().delete()

    fruits: list[Fruit] = [
        Fruit(name="Apple", price=5, quantity=100000),
        Fruit(name="Banana", price=2, quantity=100000),
        Fruit(name="Pineapple", price=4, quantity=100000),
        Fruit(name="Peach", price=3, quantity=100000)
    ]

    return Fruit.objects.bulk_create(fruits)


def create_trades(fruits: list[Fruit]):
    Trade.objects.all().delete()

    trades_to_create: list[Trade] = []

    for fruit in fruits:
        for i in range(10):
            action = Trade.Action.BUY if i % 2 == 0 else Trade.Action.SELL

            trade = Trade(
                fruit=fruit,
                quantity=random.randint(
                    *fruit.get_range(action=action, fruit_type=fruit.name)
                ),
                action=action,
                status=random.choice(list(Trade.Status))
            )

            trades_to_create.append(trade)

    Trade.objects.bulk_create(trades_to_create)


def create_balance():
    Balance.objects.all().delete()
    Balance.objects.create(value=1000000)


def create_users():
    User.objects.all().delete()

    users_to_create = [
        User(
            username=f"Joker🤡",
            password=make_password(f"Joker1-"),
        )
    ]

    for index in range(1, 10):
        users_to_create.append(
            User(
                username=f"Spacelab{index}",
                password=make_password(f"Spacelab{index}-"),
            )
        )

    User.objects.bulk_create(users_to_create)


def create_messages():
    Message.objects.all().delete()

    users = User.objects.exclude(username="Joker🤡")

    contents: list[str] = [
        "Apples have arrived at the warehouse",
        "Pineapples are sold out",
        "A new batch of peaches has arrived",
        "Bananas are in stock now",
        "Operation successfully completed",
        "Insufficient funds available",
        "Purchase operation failed",
        "Shipment has been dispatched",
        "Warehouse inventory is updated",
        "A new supply has come in",
        "The item has been sent",
        "Today's profit report",
        "Losses over the period",
        "Inventory audit is complete",
        "Data has been refreshed",
        "System error message received",
        "The order has been processed",
        "Account has been topped up",
        "Funds have been debited",
        "System alert message",
        "Stock levels have been checked",
        "Current peach quantity",
        "Total sales amount",
        "Operation was unsuccessful",
        "Financial audit performed",
        "Congratulations on the sale!",
        "New customer order received",
        "Delivery issue has occurred",
        "Connection to server was lost",
        "Invalid data provided",
        "Warehouse is ready for operations",
        "Work has been finalized",
        "Waiting for the next shipment",
        "Message has been accepted",
        "Everything is working properly",
        "Fresh apples have arrived",
        "Funds have been withdrawn",
        "Some bananas were sold",
        "Peaches are on the shelf",
        "Remaining pineapple stock"
    ]

    messages_to_create = []

    for index, content in enumerate(contents):
        messages_to_create.append(
            Message(
                author=users[index % len(users)],
                content=content
            )
        )

    Message.objects.bulk_create(messages_to_create)


def create_declarations():
    Declaration.objects.all().delete()

    datasets_dir = os.path.join(settings.BASE_DIR, 'datasets')

    for filename in os.listdir(datasets_dir):
        file_path = os.path.join(datasets_dir, filename)

        with open(file_path, 'rb') as f:
            file_object = File(f, name=filename)
            declaration = Declaration(file=file_object)
            declaration.save()


class Command(BaseCommand):
    help = "Fill database with initial data"

    def handle(self, *args, **options):
        fruits = create_fruits()
        create_trades(fruits)
        create_balance()
        create_users()
        create_messages()
        create_declarations()

        self.stdout.write(
            self.style.SUCCESS("Init project command finished successfully.")
        )
