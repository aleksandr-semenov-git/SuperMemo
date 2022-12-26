from django.contrib.auth.models import User

from account.models import Profile


class ProfileService:
    @staticmethod
    def get_or_create_profile(user: User) -> Profile:
        """Take user, return profile"""
        profile, created = Profile.objects.get_or_create(user=user)
        return profile
