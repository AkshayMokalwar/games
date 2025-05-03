from django.urls import path,re_path
import users.consumers as consumers


websocket_urlpaterns = [
    # path('uws/', consumers.GuessGameConsumer.as_asgi()),
    path("ws/gameroom/", consumers.GuessGameConsumer.as_asgi()),
]