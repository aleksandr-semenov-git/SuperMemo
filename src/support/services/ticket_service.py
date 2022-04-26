from django.contrib.auth.models import User


class TicketService:
    @staticmethod
    def find_support() -> User:
        """Find staff-user who have minimum tickets"""
        all_staff = User.objects.filter(is_staff=True)
        staff_dict = {}
        for staff in all_staff:
            ticket_count = staff.tickets.count()
            staff_dict[ticket_count] = staff.id

        sorted_ticket_count_list = sorted(staff_dict)
        support_id = staff_dict[sorted_ticket_count_list[0]]
        support = User.objects.get(pk=support_id)
        return support
