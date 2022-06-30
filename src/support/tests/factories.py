import factory.fuzzy
from django.contrib.auth.models import User

from memo.tests.factories import UserFactory
from support.models import Ticket, Message


class SupportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = 'test_support0'
    email = 'test@support.email'
    is_staff = True


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    user = factory.SubFactory(UserFactory)
    support = factory.SubFactory(SupportFactory)
    description = factory.Sequence(lambda n: 'description%d' % n)


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    text = factory.Sequence(lambda n: 'message%d' % n)
    user = factory.SubFactory(UserFactory)
    ticket = factory.SubFactory(TicketFactory)
