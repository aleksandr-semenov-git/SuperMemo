import functools
from unittest.mock import MagicMock

from support.api.api_views import TicketViewSet
from support.api.serializers import TicketSerializer
from support.services import TicketService


def trackcalls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.has_been_called = True
        return func(*args, **kwargs)
    wrapper.has_been_called = False
    return wrapper


class MockTicketServices:
    @staticmethod
    def filter_tickets_by_user_id():
        mock_ticket1 = MagicMock()
        mock_ticket2 = MagicMock()
        return [mock_ticket1, mock_ticket2]


class MockTicketSerializer:
    @staticmethod
    def new():
        test_data = {'id': 1, 'user': 1, 'support': 1}
        return MagicMock(data=test_data)


def test_tickets_list(monkeypatch):
    @trackcalls
    def mock_filter(*args, **kwargs):
        return MockTicketServices.filter_tickets_by_user_id()

    @trackcalls
    def mock_new(*args, **kwargs):
        return MockTicketSerializer.new()

    monkeypatch.setattr(TicketService, 'filter_tickets_by_user_id', mock_filter)
    monkeypatch.setattr(TicketSerializer, '__new__', mock_new)

    mock_request = MagicMock(user=MagicMock(id=11))
    view = TicketViewSet(request=mock_request)
    result = view.list(mock_request)

    assert mock_filter.has_been_called
    assert mock_new.has_been_called


