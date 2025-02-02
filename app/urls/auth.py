from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from app.views.auth import CurrentUserAPI, LoginAPI, RegisterAPI

urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="register"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("current_user/", CurrentUserAPI.as_view(), name="current-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
