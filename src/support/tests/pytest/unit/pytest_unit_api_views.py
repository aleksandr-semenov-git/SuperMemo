import functools
from unittest.mock import MagicMock

from rest_framework.response import Response

from support.api.api_views import TicketViewSet
from support.api.serializers import TicketSerializer
from support.services import TicketService

TEST_TICKET_SERIALIZER_DATA = {'id': 1, 'user': 1, 'support': 1}
TEST_USER_ID = 11


def mocktracker(func):
    """Mr. MockTracker"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.has_been_called = True
        wrapper.call_args_list = args
        wrapper.call_kwargs_list = kwargs
        catch_mock = func(*args, **kwargs)
        wrapper.mock_obj = catch_mock
        return catch_mock
    wrapper.has_been_called = False
    return wrapper


class MockTicketServices:
    @staticmethod
    def filter_tickets_by_user_id():
        return MagicMock()


class MockTicketSerializer:
    @staticmethod
    def new():
        test_data = TEST_TICKET_SERIALIZER_DATA
        mock_ticket = MagicMock(data=test_data)
        return mock_ticket


class MockResponse:
    @staticmethod
    def new(*args, **kwargs):
        status = kwargs.pop('status', None)
        return MagicMock(status=status)


def test_tickets_list(monkeypatch):
    @mocktracker
    def mock_filter(*args, **kwargs):
        return MockTicketServices.filter_tickets_by_user_id()

    @mocktracker
    def mock_new_ticket(*args, **kwargs):
        return MockTicketSerializer.new()

    @mocktracker
    def mock_new_response(*args, **kwargs):
        return MockResponse.new(*args, **kwargs)

    monkeypatch.setattr(TicketService, 'filter_tickets_by_user_id', mock_filter)
    monkeypatch.setattr(TicketSerializer, '__new__', mock_new_ticket)
    monkeypatch.setattr(Response, '__new__', mock_new_response)

    mock_request = MagicMock(user=MagicMock(id=TEST_USER_ID))
    view = TicketViewSet(request=mock_request)
    result = view.list(mock_request)

    assert result.status == 200
    assert mock_filter.has_been_called
    assert mock_filter.call_args_list == (TEST_USER_ID,)
    assert mock_filter.call_kwargs_list == {}
    assert mock_new_ticket.has_been_called
    # The only good way to test line 75 I found is to catch the Mock inside @mocktracker
    assert mock_new_ticket.call_args_list == (TicketSerializer, mock_filter.mock_obj)
    assert mock_new_ticket.call_kwargs_list == {'many': True}
    assert mock_new_response.has_been_called
    assert mock_new_response.call_args_list == (Response, TEST_TICKET_SERIALIZER_DATA, )
    assert mock_new_response.call_kwargs_list == {'status': 200}
