from django.shortcuts import get_object_or_404
from lesson.models import Lesson, Question


class QuestionService:
    @staticmethod
    def create_question(question: Question, answer: str, lesson: Lesson) -> Question:
        question = Question.objects.create(question=question, answer=answer, lesson=lesson)
        return question

    @staticmethod
    def get_question_by_id(question_id: id) -> Question:
        return get_object_or_404(Question, pk=question_id)
