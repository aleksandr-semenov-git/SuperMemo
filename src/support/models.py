from django.contrib.auth.models import User
from django.db import models

IN_PROGRESS = 'INPR'
CLOSED = 'CLSD'
FREEZE = 'FRZ'
STATUS_CHOICES = (
    (IN_PROGRESS, 'in_progress'),
    (CLOSED, 'closed'),
    (FREEZE, 'freeze'),
)


class Ticket(models.Model):
    users = models.ManyToManyField(User, related_name='tickets')
    status = models.CharField(choices=STATUS_CHOICES, max_length=11, default=IN_PROGRESS)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    # frozen_at = models.DateField(default=, null=True)
    # freeze_issue = models.CharField(choices=FREEZE_CHOICES)
    # closed_at = models.DateField(default=, null=True)


class Message(models.Model):
    text = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User, related_name='messages', verbose_name='user', on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, related_name='messages', verbose_name='ticket', on_delete=models.CASCADE)

