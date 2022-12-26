from django.db.models import QuerySet

from account.models import Profile
from lesson.models import Theme, Lesson
from memo.models import Goal


class LessonService:
    @staticmethod
    def get_lesson_by_id(lesson_id: int) -> Lesson:
        """Take lesson_id, return Lesson"""
        return Lesson.objects.get(pk=lesson_id)

    @staticmethod
    def get_lessons_by_profile(profile: Profile) -> QuerySet:
        """Take profile, return filtered queryset with all lesson which have goals which are connected to the profile"""
        return Lesson.objects.filter(goal__profile=profile)

    @staticmethod
    def get_lesson_by_theme_id(theme_id: int) -> Lesson:
        """Take theme_id, return lesson which theme have theme_id"""
        return Lesson.objects.get(theme__id=theme_id)

    @staticmethod
    def get_or_create_lesson(goal: Goal, theme: Theme) -> Lesson:
        """Take goal and theme, return existing or new lesson.

        Build lesson's name from theme_name, section_name and goal_name, then use get_or_create method.
        """
        theme_name = theme.name
        section_name = theme.section.name
        name = f'{goal.name} {section_name} {theme_name}'
        lesson, created = Lesson.objects.get_or_create(name=name, goal=goal, theme=theme)
        return lesson
