from django.urls import path

from app.views.agencies import AgencyAPI, AgencyUniqueIDAPI

urlpatterns = [
    path("", AgencyAPI.as_view(), name="agency-list-create"),
    path("<str:unique_id>/", AgencyUniqueIDAPI.as_view(), name="agency-detail"),
]
