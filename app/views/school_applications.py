from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import app.constants.msg as MSG_CONST
from app.models.applications import (ApplicationComment, ApplicationMessage,
                                     ApplicationSchool,
                                     ApplicationSchoolSection,
                                     ApplicationSchoolSubSection)
from app.serializers.school_applications import (
    ApplicationCommentCreateSerializer, ApplicationCommentSerializer,
    ApplicationMessageSerializer, ApplicationSchoolDetailSerializer,
    ApplicationSchoolListSerializer, ApplicationSchoolSectionSerializer,
    ApplicationSchoolSerializer, ApplicationSchoolSubSectionSerializer)
from app.services.base import filterObjects, process_serializer


class ApplicationSchoolAPI(APIView):
    def get(self, _, application_pk):
        fields = {"application": application_pk}
        data = filterObjects(fields, ApplicationSchool)
        serializer = ApplicationSchoolListSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req, application_pk):
        data = req.data
        data["application"] = application_pk
        return process_serializer(ApplicationSchoolSerializer, data)


class ApplicationSchoolPKAPI(APIView):
    def get(self, _, pk):
        applicationSchool = get_object_or_404(ApplicationSchool, pk=pk)
        serializer = ApplicationSchoolDetailSerializer(
            applicationSchool, read_only=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, pk):
        applicationSchool = get_object_or_404(ApplicationSchool, pk=pk)
        return process_serializer(
            ApplicationSchoolSerializer,
            req.data,
            success_status=status.HTTP_200_OK,
            original_object=applicationSchool,
        )

    def delete(self, _, pk):
        applicationSchool = get_object_or_404(ApplicationSchool, pk=pk)
        applicationSchool.delete()
        return Response(
            {"message": MSG_CONST.MSG_SCHOOL_APPLICATION_DELETD},
            status=status.HTTP_204_NO_CONTENT,
        )


class ApplicationSchoolSectionAPI(APIView):
    def get(self, application_school_pk):
        fields = {"application_school_id": application_school_pk}
        data = filterObjects(fields, ApplicationSchoolSection)
        serializer = ApplicationSchoolSectionSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req, application_school_pk):
        data = req.data
        data["application_school"] = application_school_pk
        return process_serializer(ApplicationSchoolSectionSerializer, data)


class ApplicationSchoolSectionPKAPI(APIView):
    def get(self, _, pk):
        applicationSchoolSection = get_object_or_404(ApplicationSchoolSection, pk=pk)
        serializer = ApplicationSchoolSectionSerializer(applicationSchoolSection)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, pk):
        applicationSchoolSection = get_object_or_404(ApplicationSchoolSection, pk=pk)
        return process_serializer(
            ApplicationSchoolSectionSerializer,
            data=req.data,
            success_status=status.HTTP_200_OK,
            original_object=applicationSchoolSection,
        )

    def delete(self, _, pk):
        applicationSchoolSection = get_object_or_404(ApplicationSchoolSection, pk=pk)
        applicationSchoolSection.delete()
        return Response(
            {"message": MSG_CONST.MSG_APPLICATION_SECTION_DELETED},
            status=status.HTTP_204_NO_CONTENT,
        )


class ApplicationSchoolSubSectionAPI(APIView):
    def get(self, _, application_school_pk):
        fields = {"application_school_id": application_school_pk}
        data = filterObjects(fields, ApplicationSchoolSubSection)
        serializer = ApplicationSchoolSubSectionSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req, application_school_pk):
        data = req.data
        data["application_section_id"] = application_school_pk
        return process_serializer(ApplicationSchoolSubSectionSerializer, data)


class ApplicationSchoolSubSectionPKAPI(APIView):
    def get(self, _, pk):
        applicationSchoolSubSection = get_object_or_404(
            ApplicationSchoolSubSection, pk=pk
        )
        serializer = ApplicationSchoolSubSectionSerializer(applicationSchoolSubSection)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, pk):
        applicationSchoolSubSection = get_object_or_404(
            ApplicationSchoolSubSection, pk=pk
        )
        return process_serializer(
            ApplicationSchoolSubSectionSerializer,
            req.data,
            success_status=status.HTTP_200_OK,
            original_object=applicationSchoolSubSection,
        )

    def delete(self, _, pk):
        applicationSchoolSubSection = get_object_or_404(
            ApplicationSchoolSubSection, pk=pk
        )
        applicationSchoolSubSection.delete()
        return Response(
            {"message": MSG_CONST.MSG_APPLICATION_SUBSECTION_DELETED},
            status=status.HTTP_204_NO_CONTENT,
        )


class ApplicationMessagePKAPI(APIView):
    def post(self, req, application_school_pk):
        data = req.data
        data["application_school"] = application_school_pk
        return process_serializer(ApplicationMessageSerializer, data)

    def get(self, _, application_school_pk):
        fields = {"application_school_id": application_school_pk}
        data = filterObjects(fields, ApplicationMessage)
        serializer = ApplicationMessageSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApplicationCommentAPI(APIView):
    def get(self, req):
        fields = {
            "application_school": req.GET.get("application_school"),
            "application_school_section": req.GET.get("application_school_section"),
            "application_school_sub_section": req.GET.get(
                "application_school_sub_section"
            ),
        }
        data = filterObjects(fields, ApplicationComment)
        serializer = ApplicationCommentSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        data = req.data
        data["application_school"] = (req.GET.get("application_school"),)
        data["application_school_section"] = (
            req.GET.get("application_school_section"),
        )
        data["application_school_sub_section"] = (
            req.GET.get("application_school_sub_section"),
        )
        return process_serializer(ApplicationCommentCreateSerializer, data)
