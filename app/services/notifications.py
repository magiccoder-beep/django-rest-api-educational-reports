import boto3
from django.conf import settings
from uuid import uuid4
from datetime import datetime
import app.constants.msg as MSG_CONSTANT

class NotificationService:
    def __init__(self):
        self.dynamodb = boto3.resource(
            "dynamodb",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name="us-east-1"
        )
        self.table = self.dynamodb.Table(settings.DYNAMODB_TABLE_NAME)

    def create_notification(self, title, description, receiver, notification_type):

        notification_id = str(uuid4())
        timestamp = datetime.utcnow().isoformat()

        self.table.put_item(
            Item={
                "id": notification_id,
                "title": title,
                "description": description,
                "receiver": receiver,
                "type": notification_type,
                "read": False,
                "created_at": timestamp,
            }
        )
        return {"id": notification_id, "title": title}

    def get_notifications(self, receiver):
        response = self.table.scan(
            FilterExpression="receiver = :receiver",
            ExpressionAttributeValues={":receiver": receiver},
        )
        return response.get("Items", [])

    def mark_as_read(self, notification_id):
        self.table.update_item(
            Key={"id": notification_id},
            UpdateExpression="SET #read = :read",
            ExpressionAttributeNames={"#read": "read"},
            ExpressionAttributeValues={":read": True},
        )
        return {"message": MSG_CONSTANT.MSG_NOTIFICATINO_MARKED_READ}

    def delete_notification(self, notification_id):
        self.table.delete_item(Key={"id": notification_id})
        return {"message": MSG_CONSTANT.MSG_NOTIFICATION_DELETED}
