import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
from questions.models import *
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
User = get_user_model()

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name 
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        message = GroupMessage.objects.create(
            author=self.user,
            group=self.chatroom,
            body=body
        )
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user
        }
        html = render_to_string('partials/chat_message_p.html', context=context)
        self.send(text_data=html)
    


class ConnectPeopleConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.user_channel_name = f"user_sendfriend_request{self.user.id}"
        async_to_sync(self.channel_layer.group_add)(self.user_channel_name, self.channel_name)
        self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.user_channel_name,
            self.channel_name
        )
    
    def send_request_friend(self, event):
        event = event['data_sent']
        to_user = event['to_user']
        from_user = event['from_user']
        subject = event['subject']
        body = event['body']
        friend_request_id = event['friend_request_id']

        friend_req = get_object_or_404(FriendRequest, id=friend_request_id)
        

        user_to_notification = get_object_or_404(User, id=to_user)

        all_notification = FriendRequest.objects.filter(to_user=user_to_notification).order_by('-id')[:3]
        notification_header_count = FriendRequest.objects.filter(to_user=user_to_notification, readed_request=False).count()
        context = {
            'notification_header_count': notification_header_count,
            'notification_header': all_notification,
            'all_notification': friend_req,
        }
        html = render_to_string('partials/notification_update.html', context=context)
        self.send(text_data=html)



    




class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'noti_group_name'   # here we created this group name
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name    # added group name
        )
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data="This is from server!")   ## send message to the template to check connection if made

    def disconnect(self, code):
        self.close(code)  ## close connection

    def send_notification(self, event):   # this is method we created and it is even done in models to get the notifiction in overiding save method and we can even use signals when we wanted it but we used overiding save method
        self.send(event.get(
            'value'))  # this the data we get from Connect model with method type send_notification and now we are
        # going to send it  N:B value is the key we are getting from async_to_sync(channel_layer.group_send) in models so you can call it whatever you want

