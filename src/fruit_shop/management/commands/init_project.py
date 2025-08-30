from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Fill database with initial data"

    def handle(self, *args, **options):
        users_to_create = []

        for index in range(1, 10):
            users_to_create.append(
                User(
                    username=f"Spacelab{index}",
                    password=make_password(f"Qwerty{index}-"),
                )
            )

        User.objects.bulk_create(users_to_create)

        self.stdout.write(
            self.style.SUCCESS("Init project command finished successfully.")
        )
