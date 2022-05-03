from unittest.mock import MagicMock

from rest_framework.response import Response

from support.api.api_views import TicketViewSet
from support.api.serializers import TicketSerializer
from support.services import TicketService
from support.tests.decorators import mocktracker

TEST_TICKET_SERIALIZER_DATA = {'id': 1, 'user': 1, 'support': 1}
TEST_USER_ID = 11


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
    def mock_create_ticket_serializer_obj(*args, **kwargs):
        return MockTicketSerializer.new()

    @mocktracker
    def mock_create_response_obj(*args, **kwargs):
        return MockResponse.new(*args, **kwargs)

    monkeypatch.setattr(TicketService, 'filter_tickets_by_user_id', mock_filter)
    monkeypatch.setattr(TicketSerializer, '__new__', mock_create_ticket_serializer_obj)
    monkeypatch.setattr(Response, '__new__', mock_create_response_obj)

    mock_request = MagicMock(user=MagicMock(id=TEST_USER_ID))
    view = TicketViewSet(request=mock_request)
    result = view.list(mock_request)

    assert result.status == 200
    assert mock_filter.has_been_called
    assert mock_filter.call_args_list == (TEST_USER_ID,)
    assert mock_filter.call_kwargs_list == {}
    assert mock_create_ticket_serializer_obj.has_been_called
    # The only good way to test line 75 I found is to catch the Mock inside @mocktracker
    assert mock_create_ticket_serializer_obj.call_args_list == (TicketSerializer, mock_filter.mock_obj)
    assert mock_create_ticket_serializer_obj.call_kwargs_list == {'many': True}
    assert mock_create_response_obj.has_been_called
    assert mock_create_response_obj.call_args_list == (Response, TEST_TICKET_SERIALIZER_DATA, )
    assert mock_create_response_obj.call_kwargs_list == {'status': 200}
