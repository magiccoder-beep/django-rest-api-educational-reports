from rest_framework import serializers

from app.models.school_reports import SchoolReport
from app.models.schools import School, SchoolDocument
from app.models.submissions import Submission
from app.models.users import User
from app.serializers.reports import ReportSerializer
from app.serializers.users import UserNameSerializer


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            "id",
            "name",
            "gradeserved",
            "county",
            "type",
            "state",
            "status",
            "zipcode",
            "address",
            "city",
            "district",
            "agency",
        ]
        extra_kwargs = {
            "name": {"required": False},
            "gradeserved": {"required": False},
            "county": {"required": False},
            "type": {"required": False},
            "state": {"required": False},
            "zipcode": {"required": False},
            "address": {"required": False},
            "district": {"required": False},
            "agency": {"required": False},
        }


class ListSchoolWithUserSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = [
            "id",
            "name",
            "gradeserved",
            "county",
            "type",
            "state",
            "zipcode",
            "address",
            "district",
            "status",
            "agency",
            "city",
            "users",
        ]

    def get_users(self, obj):
        users = User.objects.filter(school=obj)
        return UserNameSerializer(users, many=True).data


class SchoolNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["id", "name"]


class SubmissionSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["id", "name", "gradeserved"]


class SchoolDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolDocument
        fields = ["id", "file_url", "name", "type", "year", "created_by", "school"]


class SchoolDocumentWithSchoolSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)

    class Meta:
        model = SchoolDocument
        fields = ["id", "file_url", "name", "type", "year", "created_by", "school"]
