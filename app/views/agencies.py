from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import app.constants.msg as MSG_CONST
from app.models.agencies import Agency
from app.serializers.agencies import AgencySerializer
from app.services.base import process_serializer


class AgencyAPI(APIView):
    def get(self, _):
        agencies = Agency.objects.all()
        serializer = AgencySerializer(agencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        return process_serializer(AgencySerializer, req.data)


class AgencyUniqueIDAPI(APIView):
    def get_agency(self, _, unique_id):
        return get_object_or_404(Agency, agency_unique_id=unique_id)

    def get(self, _, unique_id):
        agency = self.get_agency(self, unique_id)
        serializer = AgencySerializer(agency)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, _, unique_id):
        agency = self.get_agency(self, unique_id)
        agency.delete()
        return Response(
            {"message": MSG_CONST.MSG_AGENCY_DELETED}, status=status.HTTP_204_NO_CONTENT
        )

    def put(self, req, unique_id):
        agency = self.get_agency(self, unique_id)
        return process_serializer(
            AgencySerializer,
            data=req.data,
            success_status=status.HTTP_200_OK,
            original_object=agency,
        )
