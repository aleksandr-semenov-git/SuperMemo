from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from memo.models import Goal
from .serializers import ProfileDetailsSerializer, UserProfileDetailsSerializer
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly, ProfileIsOwnerOrReadOnly
from account.models import Profile
from rest_framework.permissions import IsAuthenticated, IsAdminUser


# class Goals(generics.ListAPIView):
#     serializer_class = GoalSerializer
#     queryset = Goal.objects.all()


class UserProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileDetailsSerializer
    queryset = User.objects.all()
    permission_classes = (IsOwnerOrReadOnly, )


class ProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileDetailsSerializer
    queryset = Profile.objects.all()
    permission_classes = (ProfileIsOwnerOrReadOnly, IsAuthenticated)
