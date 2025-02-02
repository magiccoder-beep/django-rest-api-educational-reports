from rest_framework import serializers

from app.models.agencies import Agency


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = [
            "agency_title",
            "admin_privileges",
            "school_privileges",
            "access_school",
            "home_url",
        ]
