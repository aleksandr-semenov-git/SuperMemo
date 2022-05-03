from unittest.mock import MagicMock

from support.tests.pytest.unit.pytest_unit_api_views import TEST_TICKET_SERIALIZER_DATA


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