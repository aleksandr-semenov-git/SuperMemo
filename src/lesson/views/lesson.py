from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.http import require_POST
from memo.models import Lesson, Question, Goal, Theme, Section
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from lesson.forms import ChooseSectionForm, ChooseThemeForm, LearningForm


@method_decorator(login_required, name='dispatch')
class SurePage(View):
    def get(self, request, *args, **kwargs):
        section = Section.objects.get(pk=request.session['lesson_section_id'])
        theme = Theme.objects.get(pk=request.session['lesson_theme_id'])
        goal = Goal.objects.get(pk=request.session['goal_id'])
        return render(request, 'sure_page.html', {'goal': goal, 'section': section, 'theme': theme})

    def post(self, request, *args, **kwargs):
        return redirect('lesson:lesson_page')


@method_decorator(login_required, name='dispatch')
class LessonPage(View):
    def get(self, request, *args, **kwargs):

        profile = request.user.profile
        goal = Goal.objects.get(pk=request.session['goal_id'])
        if 'active_lesson_id' in request.session:  # Todo Пока нет декоратора active-lesson будет так
            lesson = Lesson.objects.get(pk=request.session['active_lesson_id'])
        else:
            name = goal.lessons.count() + 1  # Todo Подумать над именем урока
            lesson = Lesson.objects.create(name=name, goal=goal, profile=profile)
            request.session['active_lesson_id'] = lesson.id

        form = LearningForm()
        return render(request, 'lesson.html', {'form': form, 'lesson': lesson})

    def post(self, request, *args, **kwargs):
        form = LearningForm(request.POST)
        goal = Goal.objects.get(pk=request.session['goal_id'])
        section = Section.objects.get(pk=request.session['lesson_section_id'])
        theme = Theme.objects.get(pk=request.session['lesson_theme_id'])
        lesson = Lesson.objects.get(pk=request.session['active_lesson_id'])
        if form.is_valid():
            cd = form.cleaned_data
            question = cd['question']
            answer = cd['answer']
            new_question = Question.objects.create(question=question,
                                                   answer=answer,
                                                   lesson=lesson,
                                                   goal=goal,
                                                   section=section,
                                                   theme=theme)
            form = LearningForm()
            return render(request, 'lesson.html', {'form': form, 'lesson': lesson})
        else:
            return render(request, 'lesson.html', {'form': form, 'lesson': lesson})


@method_decorator(login_required, name='dispatch')
class EndLessonPage(View):
    def get(self, request, *args, **kwargs):
        lesson = Lesson.objects.get(pk=request.session['active_lesson_id'])
        return render(request, 'end_lesson.html', {'lesson': lesson})

    def post(self, request, *args, **kwargs):
        if request.POST.get('end') == 'End lesson':
            goal = Goal.objects.get(pk=request.session['goal_id'])
            request.session['active_lesson_id'] = False
            request.session['lesson_section_id'] = False
            request.session['lesson_theme_id'] = False
            return redirect('memo:goal_page', goal_id=goal.id)
        else:
            return redirect('lesson:lesson_page')
