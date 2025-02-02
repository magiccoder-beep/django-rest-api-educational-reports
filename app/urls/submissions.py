from django.urls import path

from app.views.submissions import (SubmissionAPI, SubmissionFilterAPI,
                                   SubmissionMessageAPI, SubmissionPKAPI, SubmissionFilterPaginatedListAPI)

urlpatterns = [
    path("filter/<str:type>/", SubmissionFilterPaginatedListAPI.as_view(), name="submission-filter"),
    path(
        "filter/<str:type>/<str:pk>/",
        SubmissionFilterAPI.as_view(),
        name="submission-filter",
    ),
    path("", SubmissionAPI.as_view(), name="submission-list-create"),
    path("<str:pk>/", SubmissionPKAPI.as_view(), name="submission-detail"),
    path(
        "messages/<str:submission_pk>/",
        SubmissionMessageAPI.as_view(),
        name="submission-message-list",
    ),
]
