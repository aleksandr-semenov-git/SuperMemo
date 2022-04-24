from django.urls import path

from support.api.api_views.ticket_views import TicketViewSet

urlpatterns = [
    path('user/get/tickets/', TicketViewSet.as_view({'get': 'list'})),
]
