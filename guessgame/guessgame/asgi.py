from channels.routing import ProtocolTypeRouter, URLRouter
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from django.urls import path
from django.core.asgi import get_asgi_application

# Consumer example
class GuessGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data="Hello from WebSocket!")

# # Routing for WebSockets
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": URLRouter([
#         path("ws/guessgame/", GuessGameConsumer.as_asgi()),  # Make sure this matches your route
#     ]),
# })

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                    path('ws/messenger/<room_id>/', GuessGameConsumer()), 
            ])
        )
    ),
})
