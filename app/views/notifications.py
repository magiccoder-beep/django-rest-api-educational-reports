from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.services.notifications import NotificationService

import app.constants.msg as MSG_CONST

notification_service = NotificationService()


class CreateNotificationView(APIView):
    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description")
        receiver = request.data.get("receiver")
        notification_type = request.data.get("type")
        
        print(title, description, receiver, notification_type)

        if not title or not receiver:
            return Response({"error": MSG_CONST.MSG_NOTIFICATION_VALIDATION['required']}, status=status.HTTP_400_BAD_REQUEST)

        notification = notification_service.create_notification(title, description, receiver, notification_type)
        return Response(notification, status=status.HTTP_201_CREATED)

class GetNotificationsView(APIView):
    def get(self, _, receiver):
        notifications = notification_service.get_notifications(receiver)
        return Response({"notifications": notifications}, status=status.HTTP_200_OK)

class MarkAsReadNotificationView(APIView):
    def post(self, _, notification_id):
        try:
            result = notification_service.mark_as_read(notification_id)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteNotificationView(APIView):
    def delete(self, _, notification_id):
        try:
            result = notification_service.delete_notification(notification_id)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
