from decimal import Decimal
from django.conf import settings
from django.db import models
from memo.models import Question, Lesson


class LessonCart:
    def __init__(self, request):
        self.session = request.session
        lesson_cart = self.session.get(settings.LESSON_SESSION_ID)
        if not lesson_cart:
            lesson_cart = self.session[settings.LESSON_SESSION_ID] = {}
        self.lesson_cart = lesson_cart

    def add(self, lesson):
        lesson_id = str(lesson.id)
        if lesson_id not in self.lesson_cart:
            self.lesson_cart[lesson_id] = {'lesson': lesson}

    def save(self):
        self.session[settings.LESSON_SESSION_ID] = self.lesson_cart
        self.session.modified = True

    def remove(self, question):
        lesson_id = str(question.id)
        if lesson_id in self.lesson_cart:
            del self.lesson_cart[lesson_id]
            self.save()

    def __iter__(self):
        lesson_ids = self.lesson_cart.keys()
        lessons = Lesson.objects.filter(id__in=lesson_ids)
        for lesson in lessons:
            self.lesson_cart[str(lesson.id)]['lesson'] = lesson

    def __len__(self):
        return sum(1 for item in self.lesson_cart.keys())

    def clear(self):
        del self.session[settings.LESSON_SESSION_ID]
        self.session.modified = True
