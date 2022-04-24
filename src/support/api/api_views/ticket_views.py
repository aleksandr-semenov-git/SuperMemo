from rest_framework import viewsets
from rest_framework.response import Response

from support.api.serializers import TicketSerializer
from support.models import Ticket


class TicketViewSet(viewsets.ViewSet):
    """"""
    def list(self, request):
        queryset = Ticket.objects.filter(users=request.user.id)
        serializer = TicketSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass
