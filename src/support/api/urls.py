from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from support.api.api_views.ticket_views import TicketViewSet

tickets_list = TicketViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = format_suffix_patterns([
    path('user/tickets/', tickets_list, name='user_tickets'),
])
