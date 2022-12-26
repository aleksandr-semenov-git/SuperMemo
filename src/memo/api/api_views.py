from rest_framework import generics
from memo.models import Goal
from .serializers import GoalSerializer


class Goals(generics.ListAPIView):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()


class GoalDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()
