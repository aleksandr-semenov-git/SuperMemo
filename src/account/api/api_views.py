from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from account.models import Profile
from .permissions import IsOwnerOrReadOnly, ProfileIsOwnerOrReadOnly
from .serializers import ProfileDetailsSerializer, UserProfileDetailsSerializer


class UserProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileDetailsSerializer
    queryset = User.objects.all()
    permission_classes = (IsOwnerOrReadOnly, )


class ProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileDetailsSerializer
    queryset = Profile.objects.all()
    permission_classes = (ProfileIsOwnerOrReadOnly, IsAuthenticated)
