from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from users.models import User
from alerts.models import Notification

from rest_framework.exceptions import ValidationError

class SyncConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        if not self.scope["user"]:
            print(self.scope["error"])
            await self.close()
        elif self.scope["user"].is_anonymous:
            print(self.scope["error"])
            await self.close()
        else:
            # Accept the connection
            await self.join_group(self.scope["user"])
            self.scope['user'].set_channel(self.channel_name)
            await self.accept()
            await self.send_json(["connection-open", "Connection Started"])
    
    async def join_group(self,user):
        await self.channel_layer.group_add(
            user.group_short,
            self.channel_name,
        )

    async def disconnect(self, code):
        if self.scope['user']:
            self.scope['user'].set_channel(None)
        await self.send_json(["connection-close", "Connection Closed"])

    async def receive_json(self, content):
        await self.send_json(["error", "Not implemented."])

    async def data_change(self, event):
        msg = ["data-change", event["message"]] 
        await self.send_json(msg)

    async def new_notification(self, event):
        await self.send_json(
            [
                "notification",
                event["message"]
            ]
        )


 