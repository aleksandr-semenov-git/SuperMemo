from rest_framework import permissions

from support.models import Message, Ticket


class IsTicketOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Ticket):
        """Check if request user is belong to the ticket. Check if request in SAFE_METHODS"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.users.filter(id=request.user.id).exists()


class IsThreadParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Message):
        """Check if request user is belong to the ticket. Check if request in SAFE_METHODS"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.ticket.users.filter(id=request.user.id).exists()
