from django.urls import path

from app.views.schools import (AgencyAdminSchoolAPI, SchoolAPI,
                               SchoolDocumentPKAPI, SchoolDocumentsAPI,
                               SchoolPKAPI, SchoolReportAPI,
                               SchoolReportDeleteAPI)

urlpatterns = [
    path(
        "agency_admin/",
        AgencyAdminSchoolAPI.as_view(),
        name="agency-admin-school-list-create",
    ),
    path(
        "documents/<str:pk>/",
        SchoolDocumentPKAPI.as_view(),
        name="school-document-detail",
    ),
    path("", SchoolAPI.as_view(), name="school-list-create"),
    path("<str:pk>/", SchoolPKAPI.as_view(), name="school-detail"),
    path(
        "<str:pk>/documents/",
        SchoolDocumentsAPI.as_view(),
        name="school-documents-list-create",
    ),
    path(
        "<str:pk>/reports/", SchoolReportAPI.as_view(), name="school-report-list-create"
    ),
    path(
        "<str:pk>/report_delete/",
        SchoolReportDeleteAPI.as_view(),
        name="school-report-list-create",
    ),
]
