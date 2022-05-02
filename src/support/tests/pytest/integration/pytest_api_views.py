import pytest
from rest_framework.response import Response
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_tickets_list(auth_client, ticket):
    result = auth_client.get(reverse('support_api:user_tickets'))
    data = dict(result.data[0])

    assert result.status_code, 200
    assert isinstance(result, Response)
    assert data['id'] == ticket.id
    assert data['description'] == ticket.description
    assert data['user'] == ticket.user.id
    assert data['support'] == ticket.support.id
