from django.urls import path
from app.views.notifications import (
    CreateNotificationView,
    GetNotificationsView,
    MarkAsReadNotificationView,
    DeleteNotificationView,
)

urlpatterns = [
    path("", CreateNotificationView.as_view(), name="create-notification"),
    path("<str:receiver>/", GetNotificationsView.as_view(), name="get-notifications"),
    path("<str:notification_id>/mark-as-read/", MarkAsReadNotificationView.as_view(), name="mark-as-read-notification"),
    path("<str:notification_id>/delete/", DeleteNotificationView.as_view(), name="delete-notification"),
]
