import json

from asgiref.sync import sync_to_async

from django.template.loader import render_to_string

from channels.generic.websocket import AsyncWebsocketConsumer

from src.fruit_shop.models import Message


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
            group=self.group_name,
            message={
                'type': 'chat_message',
                'html': message_html
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=event['html'])
