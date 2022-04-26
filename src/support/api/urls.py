from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from support.api.api_views.message_views import MessageViewSet
from support.api.api_views.ticket_views import TicketViewSet

tickets_list = TicketViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

message_list = MessageViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = format_suffix_patterns([
    path('user/tickets/', tickets_list, name='user_tickets'),
    path('user/ticket/<int:ticket_id>/messages/', message_list, name='user_messages'),
])
