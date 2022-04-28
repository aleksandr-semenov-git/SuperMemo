from rest_framework import serializers

from support.models import Ticket, Message
from support.services.ticket_service import TicketService


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    def create(self, validated_data: dict) -> Ticket:
        """Redefine create method to automatically find the most free support and add him to the ticket"""
        support = TicketService.find_support()
        new_ticket = TicketService.create_ticket(validated_data)
        new_ticket.users.set(support.id)
        return new_ticket


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    def validate(self, data: dict) -> dict:
        """
        Compare POST-request-data with user's data to check if user can leave messages in the ticket.
        It's also prevent user to somehow leave messages in a wrong ticket.
        """
        context = self.context
        if context['ticket_id'] != data['ticket'].id or context['user_id'] != data['user'].id:
            raise serializers.ValidationError('Only participant of thread can create a message on this page.')

        return super().validate(data)

