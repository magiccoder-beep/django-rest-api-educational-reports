from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.receiver = self.scope["url_route"]["kwargs"]["receiver"]
        self.group_name = f"notifications_{self.receiver}"
        print("Connected!")
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        print("Receive Text Data", text_data)
        data = json.loads(text_data)
        print(f"Received message: {data}")

        # Send the received message to the group
        await self.channel_layer.group_send(
            self.group_name,  # The group to send the message to
            {
                "type": "send_notification",  # The method name to call
                "message": data,             # The actual message
            }
        )

    async def send_notification(self, event):
        message = event["message"]
        print("Send notification", message)
        await self.send(text_data=json.dumps(message))
