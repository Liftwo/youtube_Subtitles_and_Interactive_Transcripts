from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json
import logging
from asgiref.sync import async_to_sync
from redis import Redis
from django_redis import get_redis_connection
from random import randint
from time import sleep
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from channels.db import database_sync_to_async
from django.db.models import Sum
from rest_framework import serializers


logger = logging.getLogger('django')


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'ops_coffee'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

    async def chat_message(self, event):
        message = 'talk_talk:' + event['message']
        await self.send(text_data=json.dumps({
            'message':message
        }))


class TrackConsumer(AsyncWebsocketConsumer):
    db = Redis(host='127.0.0.1', port=6379, db=0)

    async def websocket_connect(self, message):
        await self.accept()
        await self.channel_layer.group_add('users', self.channel_name)
        user = self.scope['user']
        print('登入', user)
        if user.is_authenticated:
            print('更改狀態')
            await self.update_user_status(user, True)
            await self.send_status()

    # async def websocket_receive(self, message):
    #     print("receive", message)

    async def websocket_disconnect(self, message):
        await self.channel_layer.group_discard('users', self.channel_name)
        user = self.scope['user']
        print('斷開', user)
        if user.is_authenticated:
            print('更改狀態')
            await self.update_user_status(user, False)
            await self.send_status()

    async def send_status(self):
        users = UserProfile.objects.all()
        _users = list(UserProfile.objects.all().values('user_id','status'))
        html_users = render_to_string("user.html", {'users': users})
        await self.channel_layer.group_send('users', {"type": "user_update", "event": "Change Status", "data":_users})

    async def user_update(self, event):

        await self.send(json.dumps({'data':event['data']}))

    @database_sync_to_async
    def update_user_status(self, user, status):
        return UserProfile.objects.filter(user_id=user.pk).update(status=status)

    async def redis_connect(self):
        redis_connect = get_redis_connection()
        value = redis_connect.get("asgi:group:users")
        print(value)
        await self.send(text_data=json.dumps({'online_number': value}))


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        for i in range(1000):
            self.send(json.dumps({'message': randint(1, 100)}))
            sleep(1)



class NumberOfOnline(AsyncWebsocketConsumer):
    db = Redis(host='127.0.0.1', port=8000, db=0)

    async def connect(self):
        await self.accept()
        self.room_group_name = 'users'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        redis_connect = get_redis_connection('default')
        online_number = str(redis_connect.zcard("asgi:group:users"))
        print('上線人數', online_number)
        await self.channel_layer.group_send(self.room_group_name,{'type':'online', 'message':online_number})


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('users', self.channel_name)
        user = self.scope['user']
        print('斷開', user)
        redis_connect = get_redis_connection('default')
        online_number = str(redis_connect.zcard("asgi:group:users"))
        print('上線人數', online_number)
        await self.channel_layer.group_send(self.room_group_name,{'type':'online', 'message':online_number})

    async def online(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))











