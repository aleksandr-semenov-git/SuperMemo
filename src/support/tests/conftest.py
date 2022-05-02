import pytest

from support.tests.factories import SupportFactory, MessageFactory, TicketFactory
from memo.tests.factories import UserFactory
from rest_framework.test import APIClient


@pytest.fixture
def user():
    test_user = UserFactory()
    test_user.set_password('121212ab')
    test_user.save()
    return test_user


@pytest.fixture
def support():
    test_support = SupportFactory()
    test_support.set_password('121212ab')
    test_support.save()

    return test_support


@pytest.fixture
def ticket(user, support):
    test_ticket = TicketFactory(user=user, support=support)
    return test_ticket


@pytest.fixture
def ticket_without_sup(user):
    test_ticket = TicketFactory(user=user)
    return test_ticket


@pytest.fixture
def u_message(user, ticket):
    test_message = MessageFactory(user=user, ticket=ticket)
    return test_message


@pytest.fixture
def s_message(support, ticket):
    test_message = MessageFactory(support=support, ticket=ticket)
    return test_message


@pytest.fixture
def client():
    return APIClient()
