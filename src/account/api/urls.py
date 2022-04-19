from django.urls import path
from .api_views import ProfileDetails
from django.conf import settings
from .api_views import ProfileDetails, UserProfileDetails
from django.conf.urls import include

urlpatterns = [
    path('user/profile/<int:pk>/', UserProfileDetails.as_view(), name='user_profile_details'),
    path('profile/<int:pk>/', ProfileDetails.as_view(), name='profile_details'),
]
