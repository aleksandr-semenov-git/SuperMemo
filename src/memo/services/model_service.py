from django.shortcuts import get_object_or_404
from memo.models import Goal
from account.models import Profile
from django.db.models.query import QuerySet


class GoalService:
    @staticmethod
    def get_goals_by_profile(profile: Profile) -> QuerySet:
        """Take profile, return queryset with all profile's goals"""
        return profile.goals.all()

    @staticmethod
    def get_goal_by_id(goal_id: int) -> Goal:
        """Take goal_id, return goal or raise Http404 exception"""
        return get_object_or_404(Goal, pk=goal_id)

    @staticmethod
    def get_goal_by_name(name: str) -> Goal:
        """Take name, return goal or raise Http404 exception"""
        return get_object_or_404(Goal, name=name)

    @staticmethod
    def create_goal(name: str, profile: Profile) -> Goal:
        """Take name and profile, return created goal"""
        return Goal.objects.create(name=name, profile=profile)


