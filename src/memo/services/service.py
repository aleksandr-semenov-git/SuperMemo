from django.contrib.auth.models import User
from django.db.models import Q
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

    @staticmethod
    def get_section_by_name_and_goal_id(name, goal_id):
        return Section.objects.get(Q(name=name), Q(goal__id=goal_id))

    @staticmethod
    def create_section(name: str, goal: Goal) -> Section:
        return Section.objects.create(name=name, goal=goal)


class ThemeService:
    @staticmethod
    def get_theme_by_id(theme_id: id) -> Theme:
        return get_object_or_404(Theme, pk=theme_id)

    @staticmethod
    def get_theme_by_name_and_section_id(name, section_id):
        return Theme.objects.get(Q(name=name), Q(section__id=section_id))

    @staticmethod
    def create_theme(name: str, section: Section) -> Theme:
        return Theme.objects.create(name=name, section=section)
