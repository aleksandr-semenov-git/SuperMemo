from django.contrib.auth.models import User
from memo.models import Profile, Goal, Question, Theme, Section, Lesson


class ProfileService:
    @staticmethod
    def get_or_create_profile(user: User) -> Profile:
        profile, created = Profile.objects.get_or_create(user=user)
        return profile

    @staticmethod
    def create_profile(user: User) -> Profile:
        return Profile.objects.create(user=user)

    @staticmethod
    def profile_exists(user: User) -> bool:
        return Profile.objects.filter(user=user).exists()


class GoalService:
    @staticmethod
    def get_goals_by_profile(profile: Profile):
        return profile.goals.all()
