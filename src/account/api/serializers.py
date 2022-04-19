from rest_framework import serializers
from django.contrib.auth.models import User


class UserProfileDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileDetailsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        fields = '__all__'
