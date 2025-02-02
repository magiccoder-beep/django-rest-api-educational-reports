from rest_framework import serializers

from app.models.notifications import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "title",
            "description",
            "type",
            "receiver",
            "read",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "id": {"required": False},
            "created_at": {"required": False},
            "updated_at": {"required": False},
        }