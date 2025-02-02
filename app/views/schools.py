from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

import app.constants.msg as MSG_CONST
from app.models.school_reports import SchoolReport
from app.models.schools import School, SchoolDocument
from app.models.submissions import Submission
from app.serializers.schools import (ListSchoolWithUserSerializer,
                                     SchoolDocumentSerializer,
                                     SchoolDocumentWithSchoolSerializer,
                                     SchoolSerializer)
from app.serializers.submissions import (SchoolReportCreateSerializer,
                                         SchoolReportSerializer)
from app.services.base import filterObjects, process_serializer
from app.services.school_reports import (addSchoolToReport,
                                         deleteSchoolFromReport)
from app.utils.pagination import CustomPagination


class SchoolAPI(APIView):
    def get(self, req):
        token_data = getattr(req, "token_data", None)
        agency = token_data["agency"]
        fields = {"agency": agency}
        schools = filterObjects(fields, School)
        serializer = ListSchoolWithUserSerializer(schools, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        token_data = getattr(req, "token_data", None)
        data = req.data
        data["agency"] = token_data["agency"]
        return process_serializer(SchoolSerializer, data)

class SchoolPKAPI(APIView):
    def get_school(self, _, pk):
        return get_object_or_404(School, pk=pk)

    def get_school_user(self, _, pk):
        return School.objects.prefetch_related("school_users__user").get(pk=pk)

    def get(self, _, pk):
        school = self.get_school(self, pk)
        serializer = SchoolSerializer(school, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, _, pk):
        school = self.get_school(self, pk)
        school.delete()
        return Response(
            {"message": MSG_CONST.MSG_SCHOOL_DELETED}, status=status.HTTP_204_NO_CONTENT
        )

    def put(self, req, pk):
        school = self.get_school(self, pk)
        serializer = SchoolSerializer(school, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgencyAdminSchoolAPI(ListAPIView):
    pagination_class = CustomPagination

    def get(self, req):
        token_data = getattr(req, "token_data", None)
        agency = token_data["agency"]
        queryset = School.objects.filter(agency_id=agency)
        paginator = CustomPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(queryset, req)
        serializer = ListSchoolWithUserSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class SchoolDocumentsAPI(APIView):
    def post(self, req, pk):
        token_data = getattr(req, "token_data", None)
        data = req.data
        data["created_by"] = token_data["email"]
        serializer = SchoolDocumentSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, req, pk):
        fields = {
            'school_id' : pk,
            'year' : req.GET.get('year'),
        }
        documents = filterObjects(fields, SchoolDocument)
        serializer = SchoolDocumentWithSchoolSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SchoolDocumentPKAPI(APIView):
    def get_document(self, _, pk):
        return get_object_or_404(SchoolDocument, pk=pk)

    def get(self, _, pk):
        document = self.get_document(self, pk)
        serializer = SchoolDocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, req, pk):
        document = self.get_document(self, pk)
        serializer = SchoolDocumentSerializer(document, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, _, pk):
        document = self.get_document(self, pk)
        document.delete()
        return Response(
            {"message": MSG_CONST.MSG_SCHOOL_DOCUMENT_DELETED},
            status=status.HTTP_204_NO_CONTENT,
        )


class SchoolReportAPI(APIView):
    def get(self, req, pk):
        queryset = Submission.objects.filter(school_id=pk)
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, req)
        serializer = SchoolReportSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, req, pk):
        data = req.data
        return addSchoolToReport(pk, data["report"])


class SchoolReportDeleteAPI(APIView):
    def post(self, req, pk):
        school_id = pk
        report_id = req.data.get("report")

        return deleteSchoolFromReport(school_id=school_id, report_id=report_id)