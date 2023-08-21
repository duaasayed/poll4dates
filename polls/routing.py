from django.urls import path
from .consumers import ChatConsumer, VotingConsumer

websocket_urlpatterns = [
    path('ws/chat/<uuid:guid>/', ChatConsumer.as_asgi()),
    path('ws/voting/<uuid:guid>/', VotingConsumer.as_asgi())
]