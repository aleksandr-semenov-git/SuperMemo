from django.db.models import QuerySet

from support.models import Ticket


class MessageService:

    @staticmethod
    def filter_messages_by_ticket_id(ticket_id: int) -> QuerySet:
        """Filter messages by ticket's id"""
        queryset = Ticket.objects.filter(ticket__id=ticket_id)
        return queryset
