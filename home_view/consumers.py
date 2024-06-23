import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ConnectPeopleConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = f'connect-people-{self.user.id}'
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )
        self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )
    
    def receive(self, text_data=None, bytes_data=None):
        pass

    




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

