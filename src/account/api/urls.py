from django.urls import path
from django.conf import settings
from .api_views import ProfileDetails

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetails.as_view(), name='profile_details')
]
