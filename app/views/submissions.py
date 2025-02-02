from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models.submissions import Submission, SubmissionMessage
from app.serializers.submissions import SubmissionSerializer, SubmissionMessageSerializer, SubmissionCreateAndUpdateSerializer, SubmissionMessageDetailSerializer

from app.services.school_reports import filterSchoolReports
from app.services.base import process_serializer, filterObjects
from app.services.reports import get_reports_with_multiple_submissions
from app.services.schools import get_schools_with_multiple_submissions

import app.constants.filter as FILTER_CONST

import app.constants.msg as MSG_CONST
from django.shortcuts import get_object_or_404

class SubmissionAPI(APIView):

    def get(self, req):
        fields = {
            "report_id": req.GET.get("report"),
            "school_id": req.GET.get("school"),
            "due_date": req.GET.get("due_date"),
        }
        data = filterObjects(fields, Submission)
        serializer = SubmissionCreateAndUpdateSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        return process_serializer(SubmissionCreateAndUpdateSerializer, data=req.data)


class SubmissionPKAPI(APIView):
    
    def get_submission(self, _, pk):
        return get_object_or_404(Submission, pk=pk)
    
    def get(self, _, pk):
        submission = self.get_submission(self, pk)
        serializer = SubmissionSerializer(submission, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, _, pk):
        submission = self.get_submission(self, pk)
        submission.delete()
        return Response({"message": MSG_CONST.MSG_SUBMISSION_DELETED}, status=status.HTTP_204_NO_CONTENT)
    
    def put(self, req, pk):
        submission = self.get_submission(self, pk)
        return process_serializer(SubmissionCreateAndUpdateSerializer, data=req.data, success_status=status.HTTP_200_OK, original_object=submission)


class SubmissionFilterAPI(APIView):
    
    def get(self, _, type, pk):
        data = filterSchoolReports(type, pk)
        return Response(data, status=status.HTTP_200_OK)

class SubmissionFilterPaginatedListAPI(APIView):
    
    def get(self, req, type):
        token_data = getattr(req, "token_data", None)
        selected_agency = token_data["agency"]
        page_size = int(req.GET.get("page_size", 10))
        
        function_map = {
            FILTER_CONST.SUBMISSION_FILTER_BY_REPORT: get_reports_with_multiple_submissions,
            FILTER_CONST.SUBMISSION_FILTER_BY_SCHOOL: get_schools_with_multiple_submissions
        }
        response_data = function_map[type](req, selected_agency, page_size)

        return Response(response_data, status=status.HTTP_200_OK)
        
    
class SubmissionMessageAPI(APIView):
    
    def post(self, req, submission_pk):
        data = req.data
        data['submission'] = submission_pk
        token_data = getattr(req, "token_data", None)
        data['sender'] = token_data['user_id']
        print(data)
        return process_serializer(SubmissionMessageSerializer, data)
    
    def get(self, _, submission_pk):
        fields = {
            'submission_id': submission_pk
        }
        data = filterObjects(fields, SubmissionMessage)
        serializer = SubmissionMessageDetailSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        