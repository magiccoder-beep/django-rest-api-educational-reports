from rest_framework import serializers

from app.models.submissions import Submission, SubmissionMessage
from app.serializers.reports import (ReportSerializer,
                                     SubmissionReportSerializer)
from app.serializers.schools import (SchoolNameSerializer, SchoolSerializer,
                                     SubmissionSchoolSerializer)
from app.serializers.users import UserSerializer, UserFullNameSerializer


class SubmissionSerializer(serializers.ModelSerializer):
    report = ReportSerializer(read_only=True)
    school = SchoolSerializer(read_only=True)
    assigned_member = UserSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = [
            "id",
            "agency",
            "due_date",
            "report",
            "school",
            "status",
            "assigned_member",
            "evaluator",
            "school_submission_date",
            "evaluator_submission_date",
            "school_submission_explanation",
            "file_urls",
        ]

class SubmissionCreateAndUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = [
            "id",
            "agency",
            "due_date",
            "report",
            "school",
            "status",
            "assigned_member",
            "evaluator",
            "school_submission_date",
            "evaluator_submission_date",
            "school_submission_explanation",
            "file_urls",
        ]


class SubmissionFilterBySchoolSerializer(serializers.ModelSerializer):
    report = SubmissionReportSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = [
            "id",
            "due_date",
            "report",
            "status",
            "assigned_member",
            "school_submission_date",
            "evaluator_submission_date",
        ]


class SubmissionFilterByReportSerializer(serializers.ModelSerializer):
    school = SubmissionSchoolSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = [
            "id",
            "due_date",
            "school",
            "status",
            "assigned_member",
            "school_submission_date",
            "evaluator_submission_date",
        ]


class SubmissionMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionMessage
        fields = ["id", "sender", "content", "submission", "created_at"]

class SubmissionMessageDetailSerializer(serializers.ModelSerializer):
    sender = UserFullNameSerializer(read_only=True)
    
    class Meta:
        model = SubmissionMessage
        fields = ["id", "sender", "content", "submission", "created_at"]

class SchoolReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ["school", "report"]


class SchoolReportSerializer(serializers.ModelSerializer):
    school = SchoolNameSerializer(read_only=True)
    report = ReportSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ["id", "school", "report"]
