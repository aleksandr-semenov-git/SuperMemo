from django.shortcuts import get_object_or_404
from lesson.models import Lesson, Question
from datetime import timedelta, datetime


class QuestionService:
    @staticmethod
    def create_question(question: Question, answer: str, lesson: Lesson) -> Question:
        question = Question.objects.create(question=question, answer=answer, lesson=lesson)
        return question

    @staticmethod
    def get_question_by_id(question_id: id) -> Question:
        return get_object_or_404(Question, pk=question_id)

    @staticmethod
    def cycle_to_days(self, cycle):
        days_dict = {0: 0, 1: 1, 2: 2, 3: 12, 4: 20, 5: 30, 6: 60, 7: 90, 8: 150, 9: 270, 10: 480, 11: 720, 12: 1440,
                     13: 2160, 14: 3960, 15: 6480}
        days = days_dict[cycle]
        return days

    @staticmethod
    def next_repeat_handler(self, cycle, prev_repeat_at):
        days = QuestionService.cycle_to_days(self, cycle)
        next_repeat_at = prev_repeat_at + timedelta(days=days)
        return next_repeat_at
