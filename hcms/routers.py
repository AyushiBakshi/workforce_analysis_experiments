
class conditional_router(object):
    """
    A router to control all database operations on models in all applications.
    """


from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter
from channel import channel_auth
from channel import consumers
from django.conf.urls import url

websocket_urlpatterns = [
    url(r'^api/sync$', consumers.SyncConsumer),
]

application = ProtocolTypeRouter({

    "websocket": channel_auth.TokenAuthMiddleware(
        URLRouter(websocket_urlpatterns),
    ),

})