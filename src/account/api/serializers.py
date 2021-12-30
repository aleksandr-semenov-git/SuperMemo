from rest_framework import serializers
from account.models import Profile
from django.contrib.auth.models import User

from memo.models import Goal


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'name']


