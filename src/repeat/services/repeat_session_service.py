from django.shortcuts import get_object_or_404
from lesson.models import Lesson, Question
from datetime import timedelta, datetime


class RepeatSessionService:
    @staticmethod
    def get_id_from_rep_session():
        pass