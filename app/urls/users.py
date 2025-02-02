from django.urls import path

from app.views.users import SchoolUserAPI, UserPKAPI, UserAPI, UserCreateAPI

urlpatterns = [
    path("", UserCreateAPI.as_view(), name="user-create"),
    path(
        "school_users/<str:role>/<str:school>/",
        SchoolUserAPI.as_view(),
        name="school-user-detail",
    ),
    path("agency_admin/", UserAPI.as_view(), name="user-agency-admin"),
    path("<str:pk>/", UserPKAPI.as_view(), name="user-detail"),
]
