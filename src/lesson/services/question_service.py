from datetime import date
from datetime import timedelta

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
        """Take question, answer, lesson, return question"""
        question = Question.objects.create(question=question, answer=answer, lesson=lesson)
        return question

    @staticmethod
    def get_question_by_id(question_id: id) -> Question:
        """Take question_id, return question or raise Http404 exception"""
        return get_object_or_404(Question, pk=question_id)

    @staticmethod
    def cycle_to_days(cycle: int) -> int:
        """Take question's cycle, convert it to days with help of DAYS_DICT"""
        days_dict = settings.DAYS_DICT
        days = days_dict[cycle]
        return days

    @staticmethod
    def calculate_new_cycle(cycle: int, score: int) -> int:
        """Calculate new question's cycle.

        Take question's cycle and question's qstate-score. The logic is simple. If user repeated question less then 3
        times, he will repeat this question at the next cycle. Elseif user repeated question 3 - 5 times,
        the cycle of current question will be reduced. Elseif user repeated question more then 5 times, he will repeat
        current question tomorrow. (rows 54-60)
        For questions with cycle 1 was provided a bit different logic to not get negative cycle value. (rows 61-66)
                Parameters:
                        cycle (int): integer
                        score (int): integer
                Returns:
                        new_cycle (int): integer
        """
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
    def next_repeat_handler(cycle: int, prev_repeat_at: date):
        """Calculate the day question should be repeated next time"""
        days = QuestionService.cycle_to_days(cycle)
        next_repeat_at = prev_repeat_at + timedelta(days=days)
        return next_repeat_at

    @staticmethod
    def get_today_questions_by_profile(profile: Profile) -> QuerySet:
        """Get queryset of questions which should be repeated today"""
        today_date = date.today()
        QuestionService.renew_date_of_all_forgotten_questions(profile)
        questions = Question.objects.filter(Q(lesson__goal__profile=profile) &
                                            Q(next_repeat_at=today_date))
        return questions

    @staticmethod
    def get_next_question_by_rep_session(rep_session: RepetitionSession) -> Question:
        """Get question from rep_session which should be repeated next.

        Filter rep_session's questions by today's date, sort them by edit-time (which is important to always get next
        question during repeat process) and then get question which was edited earlier.
                Parameters:
                        rep_session (RepetitionSession):
                Returns:
                        next_question (Question):
        """
        today_date = date.today()
        next_question = \
            rep_session.questions.filter(next_repeat_at=today_date).order_by('edited_at').first()
        return next_question

    @staticmethod
    def renew_date_of_all_forgotten_questions(profile: Profile):
        """Find not repeated questions and put their repeat date on today's date.

        Return updated_questions_num as a control tool for developers.
                Parameters:
                        profile (Profile): user's profile
                Returns:
                        next_question (Question):
        """
        today_date = date.today()
        yesterday_date = today_date - timedelta(days=1)
        forgotten_questions = Question.objects.filter(Q(lesson__goal__profile=profile) &
                                                      Q(next_repeat_at__lte=yesterday_date))
        for question in forgotten_questions:
            question.next_repeat_at = today_date
        updated_questions_num = Question.objects.bulk_update(forgotten_questions, ['next_repeat_at'])
        return updated_questions_num

    @staticmethod
    def save_remembered_perfectly(question: Question, profile: Profile) -> int or Exception:
        """Save question which was marked as remembered perfectly by the user.

        Get rep_session and rep_mod (rep_mod is needed to control bugs).
        Get score by question_id and rep_session_id, get current cycle, calculate new_cycle, collect statistics,
        renew prev_repeat_at attribute for today's date, calculate next_repeat_at date and set it, save question.
                Parameters:
                        question (Question):
                        profile (Profile): user's profile
                Returns:
                        rep_session_id (int): id of the current rep_session
        """
        rep_session, rep_mod = RepSessionService.get_or_create_rep_session_mix(profile=profile, questions=None)
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
            question.next_repeat_at = next_repeat_at

            # question remembered perfectly for today. save() will change question.edited_at() attribute
            question.save()

            rep_session_id = rep_session.id
            return rep_session_id
        else:
            print('ERROR REMEMBER PERFECTLY')
            # Todo: Exception

    @staticmethod
    def question_not_remembered(question: Question, profile: Profile) -> int or Exception:
        """Save question and it's score which if question was marked as not remembered clear by the user.

        Get rep_session and rep_mod (rep_mod is needed to control bugs).
        Get score by question_id and rep_session_id, change score to +1 value and save it (qstate.score). Save question.
                Parameters:
                        question (Question):
                        profile (Profile): user's profile
                Returns:
                        rep_session_id (int): id of the current rep_session
        """
        rep_session, rep_mod = RepSessionService.get_or_create_rep_session_mix(profile=profile, questions=None)
        if rep_mod == 'active_rep_exists':
            qstate = QStateService.get_qstate_by_q_id_and_rep_id(question_id=question.id,
                                                                 rep_session_id=rep_session.id)
            qstate.score += 1
            qstate.save()

            # call save() to change question.edited_at attribute
            question.save()

            rep_session_id = rep_session.id
            return rep_session_id
        else:
            print('ERROR NOT REMEMBER ')
            # Todo: Exception
