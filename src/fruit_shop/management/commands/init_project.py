from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from src.fruit_shop.models import Message


def create_users() -> list[User]:
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


def create_messages() -> list[Message]:
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


class Command(BaseCommand):
    help = "Fill database with initial data"

    def handle(self, *args, **options):
        create_users()
        create_messages()

        self.stdout.write(
            self.style.SUCCESS("Init project command finished successfully.")
        )
