from rest_framework import serializers

from app.models.reports import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "id",
            "name",
            "report",
            "file_format",
            "domain",
            "due_date",
            "completion_time",
            "description",
            "content",
            "video_url",
            "file_urls",
            "agency",
        ]
        extra_kwargs = {
            "id": {"required": False},
            "report": {"required": False},
            "file_format": {"required": False},
            "domain": {"required": False},
            "due_date": {"required": False},
            "completion_time": {"required": False},
            "content": {"required": False},
            "file_urls": {"required": False},
            "agency": {"required": False},
        }


class ReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "id",
            "name",
            "report",
            "domain",
            "due_date",
        ]


class SubmissionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "id",
            "name",
            "report",
            "domain",
            "due_date",
        ]
