from django.contrib.auth.models import User
from django.db import models

OPEN = 'OPN'
CLOSED = 'CLSD'
FREEZE = 'FRZ'
STATUS_CHOICES = (
    (OPEN, 'open'),
    (CLOSED, 'closed'),
    (FREEZE, 'freeze'),
)

LOGIN = 'LGN'
REGISTRATION = 'REG'
STOLEN_ACCOUNT = 'ACC'
OTHER = 'OTH'
ISSUE_CHOICES = (
    (LOGIN, 'problems with login'),
    (CLOSED, 'problems with registration'),
    (FREEZE, 'stolen account'),
    (OTHER, 'other issue'),
)


class Ticket(models.Model):
    user = models.ForeignKey(User, related_name='u_tickets', on_delete=models.CASCADE)
    support = models.ForeignKey(User, related_name='s_tickets', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=4, default=OPEN)
    issue = models.CharField(choices=ISSUE_CHOICES, max_length=4, default=OTHER)
    description = models.TextField(null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    text = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User, related_name='messages', verbose_name='user', on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, related_name='messages', verbose_name='ticket', on_delete=models.CASCADE)
