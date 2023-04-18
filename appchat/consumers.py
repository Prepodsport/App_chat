import json

from django.contrib.auth.models import AnonymousUser
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache.backends.locmem import _caches as cache


class ChatConsumer(AsyncWebsocketConsumer):
    # кэш добавить
    def add_cache(self):
        group = cache['us'].get(f'{self.room_name}', None)
        if group:
            group[self.channel_name] = self.user.username
        else:
            group = {self.channel_name: self.user.username}
        cache['us'][f'{self.room_name}'] = group
        return group

    # удалить кэш
    def del_cache(self):
        group = cache['us'].get(f'{self.room_name}', None)
        if group:
            if self.channel_name in group:
                del group[self.channel_name]
                if group:
                    cache['us'][f'{self.room_name}'] = group
                else:
                    del cache['us'][f'{self.room_name}']
        return group

    async def connect(self):
        print(777)
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        print(778)
        self.room_group_name = "chat_%s" % self.room_name
        print(779)
        self.user = self.scope['user']
        print(780)
        print(781)
        if self.user == AnonymousUser():
            raise DenyConnection("Нужно зарегистрироваться")
        # присоедениться к комнате
        usernames = self.add_cache()
        group_send_dict = {"type": "chat_message", "message": '👋' 'присоединился', "username": self.user.username,
                           "usernames": usernames, 'whom': 'room'}
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name, group_send_dict
        )

    async def disconnect(self, close_code):
        # Покинут комнату
        usernames = self.del_cache()
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": '🏃' 'покинул чат', "username": self.scope['user'].username,
             "usernames": usernames, 'whom': 'room'}
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Получать сообщение от WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("1")
        message = text_data_json["message"]
        print("2")
        username = text_data_json["username"]
        whom = text_data_json["whom"]
        print("4")
        print("5")
        usernames = cache['us'].get(f'{self.room_name}', None)
        print("6")
        print("7")

        print("8")
        print("9")
        await self.channel_layer.group_send(self.room_name, {
            "type": "text_message",
            "message": str(message),
            "username": username
        })
        print("10")
        # Отправить сообщение в комнату
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message, "username": username,
                                   "usernames": usernames, 'whom': whom}
        )

        print("11")

        print("12")

    # Получить сообщение от комнат

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        usernames = event["usernames"]
        whom = event["whom"]
        # сообщ в вебсокет
        if whom == 'room':
            await self.send(text_data=json.dumps({"message": message, "username": username,
                                                  "usernames": usernames, 'from': 'room'}))
        else:
            if self.channel_name == whom:
                await self.send(text_data=json.dumps({"message": message, "username": username,
                                                      "usernames": usernames, 'from': username}))

            print("13")


