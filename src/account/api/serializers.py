from rest_framework import serializers
from account.models import Profile
from django.contrib.auth.models import User

from memo.models import Goal


class UserProfileDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileDetailsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        fields = '__all__'
