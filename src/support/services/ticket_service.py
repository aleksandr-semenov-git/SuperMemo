from django.contrib.auth.models import User
from django.db.models import Count

from support.models import Ticket


class TicketService:
    @staticmethod
    def find_support() -> User:
        """Find staff-user who have minimum tickets"""
        all_staff = User.objects.filter(is_staff=True).annotate(Count('tickets', distinct=True))
        staff_dict = {}
        for staff in all_staff:
            ticket_count = staff.tickets__count
            staff_dict[ticket_count] = staff.id

        sorted_ticket_count_list = sorted(staff_dict)
        support_id = staff_dict[sorted_ticket_count_list[0]]
        support = User.objects.get(pk=support_id)
        return support

    @staticmethod
    def create_ticket(validated_data) -> Ticket:
        new_ticket = Ticket.objects.create(**validated_data)
        return new_ticket

    @staticmethod
    def get_ticket_by_id(ticket_id) -> Ticket:
        ticket = Ticket.objects.get(pk=ticket_id)
        return ticket