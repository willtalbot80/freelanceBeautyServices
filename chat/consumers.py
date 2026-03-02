import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data.get('message')
        sender_id = data.get('sender')
        recipient_id = data.get('recipient')

        # persist message
        msg = await database_sync_to_async(Message.objects.create)(
            sender_id=sender_id, recipient_id=recipient_id, text=message
        )

        payload = {
            'id': msg.id,
            'sender': sender_id,
            'recipient': recipient_id,
            'text': message,
            'timestamp': msg.timestamp.isoformat(),
        }

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': json.dumps(payload),
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=message)
