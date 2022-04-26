from rest_framework import viewsets, status
from rest_framework.response import Response

from support.api.serializers import MessageSerializer
from support.models import Message


class MessageViewSet(viewsets.ViewSet):
    """"""
    def list(self, request, ticket_id):
        queryset = Message.objects.filter(ticket__id=ticket_id)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            new_message = serializer.save()
            ticket_id = new_message.ticket.id
            queryset = Message.objects.filter(ticket__id=ticket_id)
            serializer = MessageSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
