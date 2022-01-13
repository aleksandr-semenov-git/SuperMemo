from rest_framework import serializers
from account.models import Profile
from django.contrib.auth.models import User

from memo.models import Goal


class ProfileDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
