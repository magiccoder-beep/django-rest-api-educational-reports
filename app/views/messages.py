from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models.messages import Message
from app.serializers.messages import MessageSerializer

from app.services.base import process_serializer, filterObjects
import app.constants.msg as MSG_CONST

class MessageAPI(APIView):
    def get(self, req):
        token_data = getattr(req, "token_data", None)
        fields = {
            'sender' : token_data['user_id'],
            'receiver' : req.GET.get('receiver'),
        }
        filtered_messages = filterObjects(fields, Message)
        serializer = MessageSerializer(filtered_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, req):
        token_data = getattr(req, "token_data", None)
        data = {
            'sender' : token_data['user_id'],
            'message': req.data['message'],
            'receiver': req.data['receiver'],
        }
        return process_serializer(MessageSerializer, data)
    
class MessagePKAPI(APIView):
    def get(self, _, pk):
        message = get_object_or_404(Message, pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, req, pk):
        message = get_object_or_404(Message, pk=pk)
        return process_serializer(MessageSerializer, req.data, success_status=status.HTTP_200_OK, original_object=message)

    def delete(self, _, pk):
        message = get_object_or_404(Message, pk=pk)
        message.delete()
        return Response(
            {"message": MSG_CONST.MSG_NORMAL_DELETE}, status=status.HTTP_204_NO_CONTENT
        )