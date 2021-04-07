# -*- coding: utf-8 -*-
# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer, AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def chat1_disconnect(self, close_code):
        # Leave room group
        print("断开连接")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Receive message from room group

    async def receive(self, text_data):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': '1'
            }
        )

    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=message)

    async def chat1_message(self, event):
        message = event['message']
        # Send message to WebSocket
        print(message)
        await self.send(text_data=json.dumps({
            'message': message
        }))


class OnlineConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['mind_id']
        self.room_group_name = 'online_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            {
                'type': 'chat1_message',
                'message': message
            }
        )

    async def chat2_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def receive(self, text_data):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': '1'
            }
        )
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=message)


    async def online_disconnect(self, close_code):
        # Leave room group
        print("断开连接")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
