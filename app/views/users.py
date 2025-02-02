from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

import app.constants.msg as MSG_CONST
from app.serializers.users import SchoolAssignedUserSerializer, UserSerializer
from app.utils.pagination import CustomPagination
from app.services.base import process_serializer, filterObjects

User = get_user_model()


class UserPKAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, req, pk):
        user = get_object_or_404(User, pk=pk)
        # if req.user.id != user.id:
        #     return Response(
        #         {"error": MSG_CONST.MSG_AUTH["error"]}, status=status.HTTP_403_FORBIDDEN
        #     )

        serializer = UserSerializer(user, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(
            {"message": MSG_CONST.MSG_USER_DELETED}, status=status.HTTP_200_OK
        )
    
    def get(self, req, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SchoolUserAPI(APIView):
    def get(self, req, role, school):
        paginator = CustomPagination()

        if role == "School_User":
            queryset = User.objects.filter(
                Q(role="School_User") | Q(role="School_Admin"), school__id=school
            )
        else:
            queryset = User.objects.filter(role=role, school__id=school)

        paginated_queryset = paginator.paginate_queryset(queryset, req)
        serializer = SchoolAssignedUserSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

class UserAPI(APIView):
    
    def get(self, req):
        token_data = getattr(req, "token_data", None)
        agency = token_data["agency"]
        fields = {
            'agency_id': agency
        }
        data = filterObjects(fields, User)
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserCreateAPI(APIView):
    def post(self, req):
        return process_serializer(UserSerializer, data=req.data)