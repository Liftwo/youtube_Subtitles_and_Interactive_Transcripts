from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import yt_sub.routingonline

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            yt_sub.routingonline.websocket_urlpatterns
        )
    ),
})