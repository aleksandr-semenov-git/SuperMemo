from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from lesson.services import QuestionService
from repeat.services.repeat_session_service import RepSessionService


@method_decorator(login_required, name='dispatch')
class Repeat(View):
    def get(self, request, rep_id, *args, **kwargs):
        rep_session = RepSessionService.get_rep_session_by_id(rep_id)
        next_question = QuestionService.get_next_question_by_rep_session(rep_session)
        if next_question:
            return render(request, 'repeat.html', {'question': next_question})
        else:
            RepSessionService.finish_rep_session(rep_session)


@method_decorator(login_required, name='dispatch')
class RepeatCheck(View):
    def get(self, request, question_id, *args, **kwargs):
        current_question = QuestionService.get_question_by_id(question_id)
        return render(request, 'repeat_check.html', {'question': current_question})

    def post(self, request, question_id, *args, **kwargs):
        profile = request.user.profile
        answer = request.POST.get('answer')
        question = QuestionService.get_question_by_id(question_id)
        if answer == 'Remember perfectly':
            remembered_question_id, rep_session_id = QuestionService.save_remembered_perfectly(question, profile)
            return redirect('repeat:repeat', rep_id=rep_session_id)
        else:
            ...
            # Todo: in progress
        return redirect('repeat:repeat')


@method_decorator(login_required, name='dispatch')
class RepeatMix(View):
    def get(self, request, *args, **kwargs):
        rep_mod = 'M'
        profile = request.user.profile
        questions_query = QuestionService.get_today_questions_by_profile(profile)
        if len(questions_query) > 0:
            rep_session, rep_mod = RepSessionService.get_or_create_rep_session_mix(profile,
                                                                                   questions_query,
                                                                                   rep_mod=rep_mod)
            if rep_mod == 'active_rep_exists':
                return redirect('repeat:repeat', rep_id=rep_session.id)
                # Todo: message "You have active rep session. Please finish or close it"
            else:
                return redirect('repeat:repeat', rep_id=rep_session.id)
        else:
            active_rep_session_query = RepSessionService.find_all_started_rep_sessions(profile)
            active_rep_session = RepSessionService.look_for_rep_session(active_rep_session_query)
            if active_rep_session:
                RepSessionService.finish_rep_session(active_rep_session)
            return redirect('account:profile_basic')
        # Todo: message "You have no questions to repeat today. It's time to learn"


@method_decorator(login_required, name='dispatch')
class RepeatSection(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'in_progress.html', {})


@method_decorator(login_required, name='dispatch')
class RepeatTheme(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'in_progress.html', {})


@method_decorator(login_required, name='dispatch')
class RepeatGoal(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'in_progress.html', {})
