import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path,re_path
from users import consumers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guessgame.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter([
                    path("ws/gameroom/", consumers.GuessGameConsumer.as_asgi()),
                    # re_path("ws/gameroom/(?P<room_id>\w+)/$", consumers.GuessGameConsumer.as_asgi(),

                ])
            )
        ),
    })
