from django.contrib.auth.models import User
from rest_framework import serializers

from support.models import Ticket, Message
from support.services.ticket_service import TicketService


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    def create(self, validated_data):
        users = validated_data.pop('users', None)
        # We get JSON where field `users` contain only 1 user
        user = users[0]
        support = TicketService.find_support()
        new_ticket = TicketService.create_ticket(validated_data)
        new_ticket.users.set((user.id, support.id))
        return new_ticket


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
