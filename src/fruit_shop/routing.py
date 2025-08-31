from django.urls import path

from src.fruit_shop import consumers

ws_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi())
]