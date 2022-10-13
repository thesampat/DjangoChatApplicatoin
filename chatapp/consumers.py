from cgitb import text
from tokenize import group
from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import redisUser
from .models import chats
import requests
from django.core import serializers
import datetime as dt
from django.utils import timezone
import humanize


class ChatTo(WebsocketConsumer):
    def connect(self):
        save_channel(self)
        self.notify_group = 'user_notification'
        self.self_room = 'room_'+ str(self.scope['user'])


        async_to_sync(self.channel_layer.group_add)(
            self.notify_group,
            self.channel_name
        )

        async_to_sync(self.channel_layer.group_add)(
            self.self_room,
            self.channel_name
        )

        

        self.accept()

        user_ob = redisUser.objects.filter(user=self.scope['user'])
        user_ob.update(active_status=None)

        async_to_sync(self.channel_layer.group_send)(
            self.notify_group,
            {
                'type': 'chat.system_message',
                'message': str(self.scope['user']),
                'statusDisplay': 'online',
                'msgType': 'system'
            }
        )

    def disconnect(self, close_code):
        
        
        user_ob = redisUser.objects.filter(user=self.scope['user'])
        user_ob.update(active_status=timezone.datetime.now())


        last_online = redisUser.objects.filter(user=self.scope['user']).values('active_status').get()['active_status']
        user_status = humanize.naturaltime(timezone.datetime.now(timezone.utc) - last_online)

        async_to_sync(self.channel_layer.group_send)(
            self.notify_group,
            {
                'type': 'chat.system_message',
                'message': str(self.scope['user']),
                'statusDisplay': user_status,   
                'msgType': 'system'
            }
        )
        

    def chat_system_message(self, event):
        message = {'message': event['message'], 'time': event['statusDisplay'], 'typeof': event['msgType']}

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
    


    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        print(text_data)


        to_user = text_data_json['to_user']
        from_user = text_data_json['from_user']
        recepit = str(to_user+'_'+from_user)
        recepitGroup = str(to_user+'-'+from_user)


        # save the test to the database
        if text_data_json['type'] == 'group_send': 
            chatob = chats.objects.create(receipt=recepitGroup, chat=text_data_json['message'])
        else:
            chatob = chats.objects.create(receipt=recepit, chat=text_data_json['message'])

        def myconverter(o):
            if isinstance(o, dt.datetime):
                return o.__str__()        

        time = json.dumps(chatob.time, default = myconverter)
        

        self.target_room = 'room_'+to_user        
        self.targetChannel_name = redisUser.objects.filter(user=to_user).values('channel_name').get()['channel_name']


        if text_data_json['type'] == 'group_join':
            self.groupChannel_name = redisUser.objects.filter(user=from_user).values('channel_name').get()['channel_name']
            group_name = text_data_json['to_user']
           

            async_to_sync(self.channel_layer.group_add)(
            group_name,
            self.groupChannel_name
            )

        if text_data_json['type'] == 'group_send':
            group_name = text_data_json['to_user']

            async_to_sync(self.channel_layer.group_send)(
                group_name,
                {
                    'type': 'chat.message',
                    'message': text_data_json,
                    'time': time,
                    'msgType': 'group_send',
                    'to_user':group_name,
                    'from_user': from_user
                }
            )



        if text_data_json['type'] == 'private':
            async_to_sync(self.channel_layer.group_add)(
                self.target_room,
                self.targetChannel_name
            )

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.self_room,
                {
                    'type': 'chat.message',
                    'message': text_data_json,
                    'time': time,   
                    'msgType': 'private',
                    'to_user': 'none',
                    'from_user': 'none',
                }
            )

            async_to_sync(self.channel_layer.group_send)(
                self.target_room,
                {
                    'type': 'chat.message',
                    'message': text_data_json,
                    'time':time,
                    'msgType': 'private',
                    'to_user': 'none',
                    'from_user': 'none',
                }
            )


    def chat_message(self, event):
        message = {'message': event['message'], 'time': event['time'], 'typeof':event['msgType'], 'to_user' :event['to_user'],  'from_user': event['from_user']}

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))


def save_channel(self):
    channelName = self.channel_name
    request_user = self.scope['user']

    print(request_user)
    print(self.scope)
    
    existing_user = redisUser.objects.filter(user=request_user)

    if len(existing_user) == 0:
        redisUser.objects.create(user=request_user, channel_name=channelName).save()
    else:
        existing_user.update(channel_name=channelName)



#test pull requet