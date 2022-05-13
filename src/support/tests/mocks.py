from unittest.mock import MagicMock

TEST_TICKET_SERIALIZER_DATA = {'id': 1, 'user': 1, 'support': 1}


class MockTicketServices:
    @staticmethod
    def filter_tickets_by_user_id():
        return MagicMock()


class MockTicketSerializer:
    @staticmethod
    def new():
        test_data = TEST_TICKET_SERIALIZER_DATA
        mock_ticket_serializer = MagicMock(data=test_data)
        return mock_ticket_serializer


class MockResponse:
    @staticmethod
    def new(*args, **kwargs):
        status = kwargs.pop('status', None)
        return MagicMock(status=status)
