from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
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

    @staticmethod
    def get_goal_by_id(goal_id: int) -> Goal:
        return Goal.objects.get(pk=goal_id)

    @staticmethod
    def create_goal(name: str, profile: Profile):
        return Goal.objects.create(name=name, profile=profile)


class SectionService:
    @staticmethod
    def get_section_by_id(section_id: int) -> Section:
        return get_object_or_404(Section, pk=section_id)


class ThemeService:
    @staticmethod
    def get_theme_by_id(theme_id: id) -> Theme:
        return get_object_or_404(Theme, pk=theme_id)
