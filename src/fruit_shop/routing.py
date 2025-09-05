from django.urls import path

from src.fruit_shop import consumers

ws_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
    path('ws/audit/', consumers.AuditConsumer.as_asgi()),
    path('ws/declaration/', consumers.DeclarationConsumer.as_asgi()),
    path('ws/balance/', consumers.BalanceConsumer.as_asgi()),
    path('ws/trade/', consumers.TradeConsumer.as_asgi()),
    path('ws/warehouse/<str:task_id>/', consumers.WarehouseConsumer.as_asgi()),
]