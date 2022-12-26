from rest_framework import permissions

from support.models import Message, Ticket


class IsTicketOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Ticket):
        """Check if request user is belong to the ticket. Check if request in SAFE_METHODS"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user.filter(id=request.user.id).exists()


class IsThreadParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Message):
        """Check if request user is belong to the ticket. Check if request in SAFE_METHODS"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.ticket.user.filter(id=request.user.id).exists()
