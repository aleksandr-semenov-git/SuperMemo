from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from lesson.models import Question
from lesson.services import LessonService, SectionService, ThemeService, QuestionService
from datetime import datetime


@method_decorator(login_required, name='dispatch')
class Repeat(View):
    def get(self, request, theme_id, *args, **kwargs):
        lesson = ThemeService.get_theme_by_id(theme_id).lesson
        checked_questions = request.session[f'lesson{lesson.id}']
        if LessonService.check_repeat_lesson(theme_id, checked_questions):
            redirect('account:profile')  # Todo: refactor
        else:
            question = lesson.questions.exclude(pk__in=checked_questions).first()

            return render(request, 'repeat.html', {'question': question, 'theme_id': theme_id})


@method_decorator(login_required, name='dispatch')
class RepeatCheck(View):
    def get(self, request, question_id, *args, **kwargs):
        question = QuestionService.get_question_by_id(question_id)
        lesson = question.lesson
        return render(request, 'repeat_check.html', {'question': question})

    def post(self, request, question_id, *args, **kwargs):
        question = QuestionService.get_question_by_id(question_id)
        lesson = question.lesson
        theme_id = lesson.theme.id
        request.session[f'lesson{lesson.id}'].append(question.id)
        # request.session.save()
        del request.session[f'lesson{lesson.id}']
        return redirect('lesson:lesson_repeat', theme_id=theme_id)


@method_decorator(login_required, name='dispatch')
class RepeatMix(View):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        rep_session = profile.rep_session
        if len(rep_session.questions.all()) > 0:
            return render(request, 'repeat.html', {'rep_session': rep_session})
        else:
            todays_date = datetime.now().strftime("%Y-%m-%d")
            memory_pull = Question.objects.filter(Q(lesson__theme__section__goal__profile=profile)
                                                  & Q(next_repeat_at=todays_date))
            for question in memory_pull:
                question.rep_session = rep_session
            Question.objects.bulk_update(memory_pull, ['rep_session'])
            return render(request, 'repeat.html', {'rep_session': rep_session})


@method_decorator(login_required, name='dispatch')
class RepeatSection(View):
    pass


@method_decorator(login_required, name='dispatch')
class RepeatTheme(View):
    pass


@method_decorator(login_required, name='dispatch')
class RepeatGoal(View):
    pass

