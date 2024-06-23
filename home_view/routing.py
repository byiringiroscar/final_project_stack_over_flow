from django.urls import path
from .consumers import NotificationConsumer, ConnectPeopleConsumer, ChatroomConsumer

ws_patterns = [
    path('ws/notifications/', NotificationConsumer.as_asgi()),
    path('ws/connect-people', ConnectPeopleConsumer.as_asgi()),
    path('ws/chatroom/<chatroom_name>', ChatroomConsumer.as_asgi()),
]
