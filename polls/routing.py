from django.urls import path
from .consumers import ChatConsumer, VotingConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:pk>/', ChatConsumer.as_asgi()),
    path('ws/voting/<int:pk>/', VotingConsumer.as_asgi())
]