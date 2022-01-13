from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from lesson.models import Section, Theme, Lesson, Question
from memo.models import Goal
from account.models import Profile


class SectionService:
    @staticmethod
    def get_section_by_id(section_id: int) -> Section:
        return get_object_or_404(Section, pk=section_id)

    @staticmethod
    def get_section_by_name_and_goal_id(name, goal_id) -> Section:
        return get_object_or_404(Section, Q(name=name), Q(goal__id=goal_id))

    @staticmethod
    def create_section(name: str, goal: Goal) -> Section:
        return Section.objects.create(name=name, goal=goal)


class ThemeService:
    @staticmethod
    def get_theme_by_id(theme_id: id) -> Theme:
        return get_object_or_404(Theme, pk=theme_id)

    @staticmethod
    def get_theme_by_name_and_section_id(name, section_id) -> Theme:
        return get_object_or_404(Theme, Q(name=name), Q(section__id=section_id))

    @staticmethod
    def create_theme(name: str, section: Section) -> Theme:
        return Theme.objects.create(name=name, section=section)


class LessonService:
    @staticmethod
    def get_lesson_by_id(lesson_id: int) -> Lesson:
        return Lesson.objects.get(pk=lesson_id)

    @staticmethod
    def get_lessons_by_profile(profile: Profile) -> QuerySet:
        return Lesson.objects.filter(goal__profile=profile)

    @staticmethod
    def get_or_create_lesson(name: str, goal: Goal, theme: Theme) -> Lesson:
        lesson, created = Lesson.objects.get_or_create(name=name, goal=goal, theme=theme)
        return lesson


class QuestionService:
    @staticmethod
    def create_question(question: Question, answer: str, lesson: Lesson, theme: Theme) -> Question:
        return Question.objects.create(question=question, answer=answer, lesson=lesson, theme=theme)