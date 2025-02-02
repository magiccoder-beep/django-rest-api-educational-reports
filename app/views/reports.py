from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import app.constants.msg as MSG_CONST
from app.models.reports import Report
from app.serializers.reports import ReportListSerializer, ReportSerializer
from app.services.base import process_serializer
from app.utils.pagination import CustomPagination


class ReportAPI(APIView):
    def get(self, _):
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        # return process_serializer(ReportSerializer, req.data)
        serializer = ReportSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgencyAdminReportAPI(APIView):
    pagination_class = CustomPagination

    def get(self, req):
        token_data = getattr(req, "token_data", None)
        agency = token_data["agency"]
        queryset = Report.objects.filter(agency_id=agency)
        paginator = CustomPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(queryset, req)
        serializer = ReportListSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class ReportPKAPI(APIView):
    def get_report(self, _, pk):
        return get_object_or_404(Report, pk=pk)

    def get(self, _, pk):
        report = self.get_report(self, pk)
        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, _, pk):
        report = self.get_report(self, pk)
        report.delete()
        return Response(
            {"message": MSG_CONST.MSG_REPORT_DELETED}, status=status.HTTP_204_NO_CONTENT
        )

    def put(self, req, pk):
        report = self.get_report(self, pk)
        return process_serializer(
            ReportSerializer,
            data=req.data,
            success_status=status.HTTP_200_OK,
            original_object=report,
        )
