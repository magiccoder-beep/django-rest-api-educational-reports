import uuid

from django.contrib.auth import authenticate
from rest_framework import serializers

import app.constants.msg as MSG_CONST
from app.models.users import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, label="Confirm Password")

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "title",
            "role",
            "school",
            "agency",
        ]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(MSG_CONST.MSG_USER_VALIDATION["password"])
        return data

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
            title=validated_data.get("title", ""),
            role=validated_data.get("role", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            school=validated_data.get("school", None),
            agency=validated_data.get("agency", None),
        )


# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["email"], password=data["password"])
        if user and user.is_active:
            return user
        raise serializers.ValidationError(MSG_CONST.MSG_USER_VALIDATION["credential"])
