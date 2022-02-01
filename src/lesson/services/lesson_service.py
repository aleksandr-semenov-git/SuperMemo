from django.db.models import QuerySet

from account.models import Profile
from lesson.models import Theme, Lesson
from memo.models import Goal


class LessonService:
    @staticmethod
    def get_lesson_by_id(lesson_id: int) -> Lesson:
        return Lesson.objects.get(pk=lesson_id)

    @staticmethod
    def get_lessons_by_profile(profile: Profile) -> QuerySet:
        return Lesson.objects.filter(goal__profile=profile)

    @staticmethod
    def get_lesson_by_theme_id(theme_id: int) -> Lesson:
        return Lesson.objects.get(theme__id=theme_id)

    @staticmethod
    def get_or_create_lesson(goal: Goal, theme: Theme) -> Lesson:
        theme_name = theme.name
        section_name = theme.section.name
        name = f'{goal.name} {section_name} {theme_name}'
        lesson, created = Lesson.objects.get_or_create(name=name, goal=goal, theme=theme)
        return lesson

    @staticmethod
    def check_repeat_lesson(theme_id: int, checked_questions: list) -> bool:
        questions_num = Theme.objects.get(pk=theme_id).lesson.questions.count()
        if len(checked_questions) < questions_num:
            return False
        elif len(checked_questions) == questions_num:
            return True
        else:
            pass  # Todo: raise error
