from django.urls import path
from .consumers import NotificationConsumer, ConnectPeopleConsumer

ws_patterns = [
    path('ws/notifications/', NotificationConsumer.as_asgi()),
    path('ws/connect-people', ConnectPeopleConsumer.as_asgi())
]
