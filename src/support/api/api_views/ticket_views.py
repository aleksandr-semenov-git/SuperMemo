from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from support.api.permissions import IsOwnerOrReadOnly
from support.api.serializers import TicketSerializer
from support.models import Ticket


class TicketViewSet(viewsets.ViewSet):
    """"""
    def list(self, request):
        queryset = Ticket.objects.filter(users=request.user.id)
        serializer = TicketSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == 'list' or 'create':
            permission_classes = [IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
