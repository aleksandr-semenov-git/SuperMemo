from django.shortcuts import get_object_or_404
from memo.models import Goal
from account.models import Profile
from django.db.models.query import QuerySet


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


