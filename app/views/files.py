from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from app.services.files import generate_presigned_url, generate_get_presigned_url, remove_file, generate_download_url
from app.utils.helper import generateUniqueID

class GeneratePresignedURLAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, req):
        file_name = generateUniqueID()
        file_type = req.GET.get('file_type')
        generated_url = generate_presigned_url(file_name, file_type)
        return Response(
            {"url": generated_url, "file_name": file_name}, status=status.HTTP_200_OK)

class GenerateGetPresignedURLAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, req):
        file_name = req.GET.get('file_name')
        generated_url = generate_get_presigned_url(file_name)
        return Response(generated_url, status=status.HTTP_200_OK)

class GenerateDownloadPresignedUrl(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, req):
        file_name = req.GET.get('file_name')
        generated_url = generate_download_url(file_name)
        return Response(generated_url, status=status.HTTP_200_OK)

class RemoveFileAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, req):
        file_name = req.GET.get("file_name")
        result = remove_file(file_name)
        return Response(result, status=status.HTTP_200_OK)