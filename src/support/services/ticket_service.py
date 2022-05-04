from django.contrib.auth.models import User
from django.db.models import Count, QuerySet, Q

from support.models import Ticket


class TicketService:
    @staticmethod
    def find_support() -> User:
        """Find staff-user who have minimum tickets"""
        all_staff = User.objects.filter(is_staff=True).annotate(
            num_apn_tickets=Count('s_tickets', filter=Q(s_tickets__status=True)))
        support = all_staff.order_by('s_tickets__count').first()
        return support

    @staticmethod
    def create_ticket(validated_data: dict, support: User) -> Ticket:
        """Create new ticket"""
        new_ticket = Ticket.objects.create(support=support, **validated_data)
        return new_ticket

    @staticmethod
    def get_ticket_by_id(ticket_id: int) -> Ticket:
        """Get ticket by it's id"""
        ticket = Ticket.objects.get(pk=ticket_id)
        return ticket

    @staticmethod
    def filter_tickets_by_user_id(user_id: int) -> QuerySet:
        """Filter tickets by user's id"""
        queryset = Ticket.objects.filter(user__id=user_id)
        return queryset
