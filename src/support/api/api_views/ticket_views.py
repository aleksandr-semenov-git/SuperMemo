from django.http import HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.reverse import reverse

from support.api.permissions import IsOwnerOrReadOnly
from support.api.serializers import TicketSerializer
from support.models import Ticket


class TicketViewSet(viewsets.ViewSet):
    """"""
    def list(self, request):
        queryset = Ticket.objects.filter(users=request.user.id)
        serializer = TicketSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            new_ticket = serializer.save()
            ticket_id = new_ticket.id
            return HttpResponseRedirect(reverse('support_api:user_messages', kwargs={'ticket_id': ticket_id}))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == 'list' or 'create':
            permission_classes = [IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
