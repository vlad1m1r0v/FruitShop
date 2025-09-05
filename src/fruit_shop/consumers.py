import json

from asgiref.sync import sync_to_async

from django.template.loader import render_to_string

from channels.generic.websocket import AsyncWebsocketConsumer

from src.fruit_shop.models import (
    Message,
    Trade
)


class ChatConsumer(AsyncWebsocketConsumer):
    group_name = 'chat'

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        messages = await sync_to_async(
            lambda: list(Message.objects.order_by('-timestamp').select_related('author')[:40])
        )()

        history_html = await sync_to_async(render_to_string)(
            template_name='partials/messages_list.html',
            context={'messages': reversed(messages)}
        )

        await self.send(text_data=history_html)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        content = data.get('message', '').strip()
        user = self.scope['user']

        created_message = await sync_to_async(Message.objects.create)(
            author=user,
            content=content
        )

        query = lambda: Message.objects.select_related('author').get(pk=created_message.id)
        message = await sync_to_async(query)()

        message_html = await sync_to_async(render_to_string)(
            template_name='partials/messages_list.html',
            context={'messages': [message]}
        )

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'html': message_html
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=event['html'])


class AuditConsumer(AsyncWebsocketConsumer):
    group_name = 'audit'

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def progress_update(self, event):
        await self.send(text_data=json.dumps({"progress": event["progress"]}))


class DeclarationConsumer(AsyncWebsocketConsumer):
    group_name = 'declaration'

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def declaration_upload(self, event):
        today_count = event['today_count']

        count_html = await sync_to_async(render_to_string)(
            template_name='partials/declarations_count.html',
            context={'today_count': today_count}
        )

        await self.send(text_data=count_html)


class BalanceConsumer(AsyncWebsocketConsumer):
    group_name = 'balance'

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def balance_update(self, event):
        balance = event['balance']

        balance_html = await sync_to_async(render_to_string)(
            template_name='partials/balance.html',
            context={'balance': balance}
        )

        await self.send(text_data=balance_html)


class TradeConsumer(AsyncWebsocketConsumer):
    group_name = 'trade'

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        trades = await sync_to_async(
            lambda: list(Trade.objects.order_by('-timestamp').select_related('fruit'))
        )()

        trades_html = await sync_to_async(render_to_string)(
            template_name='partials/trade_log.html',
            context={'trades': reversed(trades)}
        )

        await self.send(text_data=trades_html)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def trade_log(self, event):
        query = lambda: Trade.objects.select_related('fruit').get(pk=event.get("id"))
        trade = await sync_to_async(query)()

        trades_html = await sync_to_async(render_to_string)(
            template_name='partials/trade_log.html',
            context={'trades': [trade]}
        )

        await self.send(text_data=trades_html)


class WarehouseConsumer(AsyncWebsocketConsumer):
    async def checking_finished(self, _event):
        await self.send(json.dumps({"status": "Finished"}))

    async def checking_started(self, _event):
        await self.send(json.dumps({"status": "Started"}))

    async def connect(self):
        await super().connect()

        task_id = self.scope.get("url_route").get("kwargs").get("task_id")

        await self.channel_layer.group_add(task_id, self.channel_name)

        await self.channel_layer.group_send(task_id, {"type": "checking_started"})

    async def disconnect(self, close_code):
        await self.close()
