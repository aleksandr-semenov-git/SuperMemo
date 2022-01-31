from datetime import date
from datetime import timedelta, datetime

from django.conf import settings
from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404

from account.models import Profile
from lesson.models import Lesson, Question
from repeat.models import RepetitionSession
from repeat.services import RepSessionService, QStateService


class QuestionService:
    @staticmethod
    def create_question(question: Question, answer: str, lesson: Lesson) -> Question:
        question = Question.objects.create(question=question, answer=answer, lesson=lesson)
        return question

    @staticmethod
    def get_question_by_id(question_id: id) -> Question:
        return get_object_or_404(Question, pk=question_id)

    @staticmethod
    def cycle_to_days(cycle):
        days_dict = settings.DAYS_DICT
        days = days_dict[cycle]
        return days

    @staticmethod
    def calculate_new_cycle(cycle: int, score: int) -> int:
        new_cycle = cycle
        if cycle > 1:
            if score < 3:
                new_cycle += 1
            elif 3 <= score <= 5:
                new_cycle -= 1
            elif score > 5:
                new_cycle = 1
        elif cycle == 1 and score < 3:
            cycle += 1
        elif cycle == 1 and score >= 3:
            pass
        else:
            new_cycle = 1
        return new_cycle

    @staticmethod
    def next_repeat_handler(cycle, prev_repeat_at):
        days = QuestionService.cycle_to_days(cycle)
        next_repeat_at = prev_repeat_at + timedelta(days=days)
        return next_repeat_at

    @staticmethod
    def get_today_questions_by_profile(profile: Profile) -> QuerySet:
        today_date = date.today()
        QuestionService.renew_date_of_all_forgotten_questions(profile)
        questions = Question.objects.filter(Q(lesson__goal__profile=profile) &
                                            Q(next_repeat_at=today_date))
        return questions

    @staticmethod
    def get_next_question_by_rep_session(rep_session: RepetitionSession) -> Question:
        today_date = datetime.now().today()
        yesterday_date = today_date - timedelta(days=1)
        tomorrow_date = today_date + timedelta(days=1)
        next_question = \
            rep_session.questions.filter(Q(next_repeat_at__lte=tomorrow_date) &
                                         Q(next_repeat_at__gte=yesterday_date)).order_by('edited_at').first()
        return next_question

    @staticmethod
    def renew_date_of_all_forgotten_questions(profile: Profile):
        today_date = datetime.now().today()
        forgotten_questions = Question.objects.filter(Q(lesson__goal__profile=profile) &
                                                      Q(next_repeat_at__lte=today_date))
        for question in forgotten_questions:
            question.next_repeat_at = today_date
        updated_questions_num = Question.objects.bulk_update(forgotten_questions, ['next_repeat_at'])
        return updated_questions_num

    @staticmethod
    def remember_perfectly(question: Question, profile: Profile):
        rep_session, rep_mod = RepSessionService.get_or_create_rep_session_mix(profile=profile, questions=QuerySet())
        if rep_mod == 'active_rep_exists':
            score = QStateService.get_qstate_by_q_id_and_rep_id(question_id=question.id,
                                                                rep_session_id=rep_session.id).score
            cycle = question.cycle
            new_cycle = QuestionService.calculate_new_cycle(cycle, score)
            # success. question's previous repeat date is today
            question.repeated_num += score
            question.prev_repeat_at = question.next_repeat_at
            prev_repeat_at = question.prev_repeat_at
            next_repeat_at = QuestionService.next_repeat_handler(new_cycle, prev_repeat_at)
            a = 1
            # Todo: in progress
        else:
            print('ERROR REMEMBER PERFECTLY')
            # Todo: Exception
