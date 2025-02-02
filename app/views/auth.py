from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from app.serializers.auth import LoginSerializer, RegisterSerializer
from app.serializers.users import UserSerializer

User = get_user_model()


class RegisterAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: UserSerializer,
            400: "Bad request",
        },
    )
    def post(self, req):
        serializer = self.get_serializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            201: UserSerializer,
            400: "Bad request",
        },
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        access_token["user_id"] = user.id
        access_token["email"] = user.email
        access_token["role"] = user.role
        access_token["school"] = None
        access_token["agency"] = None
        print("Init Token", user.id)

        if user.school is not None:
            access_token["school"] = user.school.id
        if user.agency is not None:
            access_token["agency"] = user.agency.agency_title

        return Response(
            {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(access_token),
            }
        )


class CurrentUserAPI(APIView):
    def get(self, req):
        token_data = getattr(req, "token_data", None)
        user_id = token_data["user_id"]
        currentUser = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(currentUser)
        return Response(serializer.data, status=status.HTTP_200_OK)
