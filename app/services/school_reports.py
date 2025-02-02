from rest_framework import status
from rest_framework.response import Response

import app.constants.filter as FILTER_CONST
import app.constants.msg as MSG_CONST
from app.models.submissions import Submission
from app.serializers.submissions import (SchoolReportCreateSerializer,
                                         SchoolReportSerializer,
                                         SubmissionFilterByReportSerializer,
                                         SubmissionFilterBySchoolSerializer)


def deleteSchoolFromReport(school_id, report_id):
    if not report_id:
        return Response(
            {"error": MSG_CONST.MSG_REPORT_ID_REQUIRED},
            status=status.HTTP_400_BAD_REQUEST,
        )

    report = Submission.objects.filter(school_id=school_id, report_id=report_id).first()

    if report:
        report.delete()
        return Response(
            {"message": MSG_CONST.MSG_REPORT_DELETED}, status=status.HTTP_204_NO_CONTENT
        )
    else:
        return Response(
            {"error": MSG_CONST.MSG_REPORT_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND
        )


def addSchoolToReport(school_id, report_id):
    data = {}
    data["report"] = report_id
    data["school"] = school_id
    serializer = SchoolReportCreateSerializer(data=data, partial=True)
    if serializer.is_valid():
        instance = serializer.save()
        return Response(
            SchoolReportSerializer(instance).data, status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def filterSchoolReports(filter_type, filter_id):
    filtered_data = []
    serializer = None

    if filter_type == FILTER_CONST.SUBMISSION_FILTER_BY_SCHOOL:
        filtered_data = Submission.objects.filter(school_id=filter_id)
        serializer = SubmissionFilterBySchoolSerializer(filtered_data, many=True)
    elif filter_type == FILTER_CONST.SUBMISSION_FILTER_BY_REPORT:
        filtered_data = Submission.objects.filter(report_id=filter_id)
        serializer = SubmissionFilterByReportSerializer(filtered_data, many=True)

    return serializer.data
