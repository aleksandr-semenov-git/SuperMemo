from rest_framework import generics
from memo.models import Goal
from .serializers import ProfileDetailsSerializer
from django.contrib.auth.models import User


# class Goals(generics.ListAPIView):
#     serializer_class = GoalSerializer
#     queryset = Goal.objects.all()


class ProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileDetailsSerializer
    queryset = User.objects.all()
