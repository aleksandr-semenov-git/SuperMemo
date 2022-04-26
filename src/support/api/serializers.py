from django.contrib.auth.models import User
from rest_framework import serializers

from support.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    def create(self, validated_data):
        users = validated_data.get("users", None)
        validated_data.pop("users")
        # We get JSON where field `users` contain only 1 user
        user = users[0]
        support = SupportService.find_support()
        new_ticket = Ticket.objects.create(**validated_data)
        new_ticket.users.set((user.id, support.id))
        return new_ticket

