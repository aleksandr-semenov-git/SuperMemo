from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from support.api.permissions import IsTicketOwnerOrReadOnly
from support.api.serializers import TicketSerializer
from support.models import Ticket


class TicketViewSet(viewsets.ViewSet):
    def list(self, request) -> HttpResponse:
        """Common viewset list method"""
        queryset = Ticket.objects.filter(users=request.user.id)
        serializer = TicketSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request) -> HttpResponse:
        """
        Redirect user to ticket's messages or show errors after validation.
        Toss ticket_id into the serializer to give extra validation options.
        """
        serializer = TicketSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            new_ticket = serializer.save()
            ticket_id = new_ticket.id
            return HttpResponseRedirect(reverse('support_api:user_messages', kwargs={'ticket_id': ticket_id}))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        """Check user's permissions"""
        if self.action in ('list', 'create'):
            permission_classes = [IsAuthenticated, IsTicketOwnerOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
