from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from memo.models import Profile, Goal
from django.db.models.query import QuerySet


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
    def get_goals_by_profile(profile: Profile) -> QuerySet:
        return profile.goals.all()

    @staticmethod
    def get_goal_by_id(goal_id: int) -> Goal:
        return get_object_or_404(Goal, pk=goal_id)

    @staticmethod
    def create_goal(name: str, profile: Profile) -> Goal:
        return Goal.objects.create(name=name, profile=profile)


