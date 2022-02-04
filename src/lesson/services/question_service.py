from datetime import date
from datetime import timedelta

from django.conf import settings
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from account.models import Profile
from lesson.models import Lesson, Question
from repeat.models import RepetitionSession


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
        current question tomorrow.
        For questions with cycle 1 was provided a bit different logic to not get negative cycle value.

        Parameters
        ----------
        cycle : int
        score : int

        Returns
        -------
        new_cycle : int
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
        """Get queryset of questions which should be repeated today and also forgotten questions"""
        today_date = date.today()
        QuestionService.renew_date_of_all_forgotten_questions(profile)
        questions = Question.objects.filter(lesson__goal__profile=profile, next_repeat_at=today_date)
        return questions

    @staticmethod
    def get_next_question_by_rep_session(rep_session: RepetitionSession) -> Question:
        """Get question which should be repeated next from the rep_session.

        Filter rep_session's questions by today's date, sort them by edit-time (which is important to always get next
        question during repeat process) and then get question which was edited earlier.
        Parameters
        ----------
        rep_session : RepetitionSession

        Returns
        -------
        next_question : Question
        """
        today_date = date.today()
        next_question = rep_session.questions.filter(
            next_repeat_at=today_date).order_by('edited_at').first()
        return next_question

    @staticmethod
    def renew_date_of_all_forgotten_questions(profile: Profile):
        """Find not repeated questions and put their next_repeat_at value on today's date.

        Return updated_questions_num as a control tool for developers.

        Parameters
        ----------
        profile : Profile

        Returns
        -------
        next_question : Question
        """
        today_date = date.today()
        yesterday_date = today_date - timedelta(days=1)
        forgotten_questions = Question.objects.filter(lesson__goal__profile=profile, next_repeat_at__lte=yesterday_date)
        for question in forgotten_questions:
            question.next_repeat_at = today_date
        updated_questions_num = Question.objects.bulk_update(forgotten_questions, ['next_repeat_at'])
        return updated_questions_num

    @staticmethod
    def save_remembered_question(question: Question, score: int):
        """Save question which was marked as remembered by the user.

        Use score to calculate new cycle. Edit question's attributes such as prev_repeat_at, next_repeat_at and
        repeated_num.

        Parameters
        ----------
        question : Question
        score : int

        Returns
        -------
        rep_session_id (int): id of the current rep_session
        """
        cycle = question.cycle
        new_cycle = QuestionService.calculate_new_cycle(cycle, score)

        # success. question's previous repeat date became today's date
        question.prev_repeat_at = question.next_repeat_at
        prev_repeat_at = question.prev_repeat_at
        next_repeat_at = QuestionService.next_repeat_handler(new_cycle, prev_repeat_at)
        question.next_repeat_at = next_repeat_at
        question.repeated_num += score

        question.save()
