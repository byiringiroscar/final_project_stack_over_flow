import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'noti_group_name'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data="This is from server!")

    def disconnect(self, code):
        self.close(code)

    def send_notification(self, event):
        self.send(event.get(
            'value'))  # this the data we get from Connect model with method type send_notification and now we are
        # going to send it  N:B value is the key we are getting from async_to_sync(channel_layer.group_send) in models so you can call it whatever you want

