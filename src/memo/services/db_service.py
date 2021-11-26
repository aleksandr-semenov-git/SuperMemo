from memo.models import Profile, Goal, Question, Theme, Section, Lesson
from abc import ABC, abstractmethod


def profile_exists(user):
    return Profile.objects.filter(user=user).exists()


def create_profile(user):
    return Profile.objects.create(user=user)


def get_goals_by_profile(profile):
    return profile.goals.all()


class DBHandlers(ABC):
    class ProfileHandler:
        @staticmethod
        def profile_exists(user):
            return Profile.objects.filter(user=user).exists()

        @staticmethod
        def create_profile(user):
            return Profile.objects.create(user=user)

    class GoalHandler:
        @staticmethod
        def get_goals_by_profile(profile):
            return profile.goals.all()


