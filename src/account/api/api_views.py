from rest_framework import generics
from .serializers import ProfileDetailsSerializer
from django.contrib.auth.models import User


class ProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileDetailsSerializer
    queryset = User.objects.all()
