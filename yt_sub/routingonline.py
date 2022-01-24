from django.urls import path
from yt_sub.consumers import ChatConsumer, WSConsumer, TrackConsumer, NumberOfOnline

websocket_urlpatterns = [
    path('ws/online_number/', NumberOfOnline.as_asgi()),
    path('ws/realtime/', WSConsumer.as_asgi()),
]
