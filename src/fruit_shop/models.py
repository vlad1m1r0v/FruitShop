from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Declaration(models.Model):
    file = models.FileField(upload_to="declarations/")
    timestamp = models.DateTimeField(auto_now_add=True)