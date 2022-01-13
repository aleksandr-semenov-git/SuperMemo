from django.urls import path
from django.conf import settings
from .api_views import Goals, GoalDetails

urlpatterns = [
    path('goals/', Goals.as_view(), name='goals'),
    path('goal/<int:pk>/', GoalDetails.as_view(), name='goal_details')
]
