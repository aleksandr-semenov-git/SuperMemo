from django.http import HttpResponseRedirect, HttpResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.reverse import reverse

from support.api.permissions import IsThreadParticipant
from support.api.serializers import MessageSerializer
from support.models import Message
from support.services import TicketService


class MessageViewSet(viewsets.ViewSet):
    def list(self, request, ticket_id: int) -> HttpResponse:
        """Common viewset list method"""
        queryset = Message.objects.filter(ticket__id=ticket_id)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, ticket_id: int) -> HttpResponse:
        """
        Redirect user to ticket's messages or show errors after validation.
        Toss ticket_id and user_id into the serializer to give extra validation options.
        """
        user_id = request.user.id
        ticket_id = TicketService.get_ticket_by_id(ticket_id).id
        serializer = MessageSerializer(data=request.data, context={'user_id': user_id, 'ticket_id': ticket_id})
        if serializer.is_valid():
            new_message = serializer.save()
            ticket_id = new_message.ticket.id
            return HttpResponseRedirect(reverse('support_api:user_messages', kwargs={'ticket_id': ticket_id}))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self) -> list:
        """Check user's permissions"""
        if self.action in ('list', 'create'):
            permission_classes = [IsAuthenticated, IsThreadParticipant]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
