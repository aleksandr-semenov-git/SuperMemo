from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from lesson.services import QuestionService
from repeat.models import RepetitionSession
from repeat.services import QStateService
from repeat.services.repeat_session_service import RepSessionService


@method_decorator(login_required, name='dispatch')
class Repeat(View):
    def get(self, request, rep_id, *args, **kwargs):
        """Render page. User repeat questions from the repeat_session one by one while not remember them all.

        User see the next_question and trying to find an answer in his mind.
        If user has remembered the all questions he will be redirected to the profile page.
        """
        rep_session = RepSessionService.get_rep_session_by_id(rep_id)
        next_question = QuestionService.get_next_question_by_rep_session(rep_session)
        if next_question:
            return render(request, 'repeat.html', {'question': next_question})
        else:
            RepSessionService.finish_rep_session(rep_session)
            return redirect('account:profile_basic')
        # Todo in v2.0: add time_spent_for_learning


@method_decorator(login_required, name='dispatch')
class RepeatCheck(View):
    def get(self, request, question_id, *args, **kwargs):
        """Render page. User see the answer. He decide is question remembered or not and then press decision-button"""
        current_question = QuestionService.get_question_by_id(question_id)
        return render(request, 'repeat_check.html', {'question': current_question})


@method_decorator(login_required, name='dispatch')
class Remember(View):
    def post(self, request, question_id, *args, **kwargs):
        """Processing user's answer and redirect to the repeat page"""
        profile = request.user.profile
        question = QuestionService.get_question_by_id(question_id)
        rep_session = RepSessionService.get_rep_session_in_progress(profile)
        rep_session_id = rep_session.id
        question_id = question.id

        score = QStateService.get_qstate_by_q_id_and_rep_id(question_id=question_id, rep_id=rep_session_id).score
        QuestionService.save_remembered_question(question, score)
        return redirect('repeat:repeat', rep_id=rep_session_id)


@method_decorator(login_required, name='dispatch')
class NotRemember(View):
    def post(self, request, question_id, *args, **kwargs):
        """Processing user's answer and redirect to the repeat page"""
        profile = request.user.profile
        question = QuestionService.get_question_by_id(question_id)
        rep_session = RepSessionService.get_rep_session_in_progress(profile)
        rep_session_id = rep_session.id
        question_id = question.id

        qstate = QStateService.get_qstate_by_q_id_and_rep_id(question_id=question_id, rep_id=rep_session_id)
        qstate.score += 1
        qstate.save()

        question.save()
        return redirect('repeat:repeat', rep_id=rep_session_id)


@method_decorator(login_required, name='dispatch')
class RepeatMix(View):
    def get(self, request, *args, **kwargs):
        """Get existing or create rep_session and redirect user to the repeat page. (row 57-65)

        If user have no questions to repeat on today, view check profile for started rep_sessions and finish them.
        After that view redirects user to the profile.
        """
        # ------------------------------------------decorator?----------------------------------------------------------
        profile = request.user.profile
        active_rep_session = RepSessionService.get_rep_session_in_progress(profile)
        if active_rep_session:
            return redirect('repeat:repeat', rep_id=active_rep_session.id)
        # --------------------------------------------------------------------------------------------------------------
        # Todo: message "You have active rep session. Please it first"
        else:
            rep_mod = RepetitionSession.MIX_MOD
            questions_query = QuestionService.get_today_questions_by_profile(profile)
            rep_session = RepSessionService.create_rep_session_in_progress(profile, rep_mod, questions_query)
            return redirect('repeat:repeat', rep_id=rep_session.id)


@method_decorator(login_required, name='dispatch')
class RepeatSection(View):
    # Todo: in progress
    def get(self, request, *args, **kwargs):
        return render(request, 'in_progress.html', {})


@method_decorator(login_required, name='dispatch')
class RepeatTheme(View):
    # Todo: in progress
    def get(self, request, *args, **kwargs):
        return render(request, 'in_progress.html', {})


@method_decorator(login_required, name='dispatch')
class RepeatGoal(View):
    # Todo: in progress
    def get(self, request, *args, **kwargs):
        return render(request, 'in_progress.html', {})
