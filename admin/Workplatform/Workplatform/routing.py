# -*- coding: utf-8 -*-
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import mind.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            mind.routing.websocket_urlpatterns
        )
    ),
})
