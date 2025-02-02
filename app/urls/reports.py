from django.urls import path

from app.views.reports import AgencyAdminReportAPI, ReportAPI, ReportPKAPI

urlpatterns = [
    path(
        "agency_admin/",
        AgencyAdminReportAPI.as_view(),
        name="agency-admin-report-list-create",
    ),
    path("", ReportAPI.as_view(), name="report-list-create"),
    path("<str:pk>/", ReportPKAPI.as_view(), name="report-detail"),
]
