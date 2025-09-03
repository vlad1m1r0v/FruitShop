from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Declaration(models.Model):
    file = models.FileField(upload_to="declarations/")
    timestamp = models.DateTimeField(auto_now_add=True)


class Fruit(models.Model):
    class Type(models.TextChoices):
        APPLE = "Apple"
        BANANA = "Banana"
        PINEAPPLE = "Pineapple"
        PEACH = "Peach"

    name = models.CharField(max_length=50, choices=Type.choices, unique=True)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)

    BUY_PRICE = {
        Type.APPLE: 4,
        Type.BANANA: 1,
        Type.PINEAPPLE: 3,
        Type.PEACH: 2,
    }

    SELL_PRICE = {
        Type.APPLE: 5,
        Type.BANANA: 2,
        Type.PINEAPPLE: 4,
        Type.PEACH: 3,
    }

    BUY_RANGE = {
        Type.APPLE: (1, 10),
        Type.BANANA: (10, 20),
        Type.PINEAPPLE: (1, 10),
        Type.PEACH: (5, 15),
    }

    SELL_RANGE = {
        Type.APPLE: (1, 10),
        Type.BANANA: (1, 30),
        Type.PINEAPPLE: (1, 10),
        Type.PEACH: (1, 20),
    }

    @classmethod
    def get_buy_price(cls, fruit_type):
        return cls.BUY_PRICE[fruit_type]

    @classmethod
    def get_sell_price(cls, fruit_type):
        return cls.SELL_PRICE[fruit_type]

    @classmethod
    def get_range(cls, action, fruit_type):
        if action == "Buy":
            return cls.BUY_RANGE[fruit_type]
        return cls.SELL_RANGE[fruit_type]


class Trade(models.Model):
    class Action(models.TextChoices):
        BUY = "Buy"
        SELL = "Sell"

    class Status(models.TextChoices):
        SUCCESS = "Success"
        ERROR = "Error"

    action = models.CharField(choices=Action.choices)
    status = models.CharField(choices=Status.choices, default=Status.SUCCESS)
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Balance(models.Model):
    value = models.PositiveIntegerField()
