from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from memo.models import Lesson, Question, Goal, Theme, Section
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from lesson.forms import ChooseSectionForm, ChooseThemeForm, LearningForm
from memo.services import GoalService, SectionService, ThemeService


@method_decorator(login_required, name='dispatch')
class SurePage(View):
    def get(self, request, *args, **kwargs):
        section = SectionService.get_section_by_id(request.session['lesson_section_id'])
        theme = ThemeService.get_theme_by_id(request.session['lesson_theme_id'])
        goal = GoalService.get_goal_by_id(request.session['goal_id'])
        return render(request, 'sure_page.html', {'goal': goal, 'section': section, 'theme': theme})

    def post(self, request, *args, **kwargs):
        return redirect('lesson:lesson_page')


@method_decorator(login_required, name='dispatch')
class LessonPage(View):
    def get(self, request, *args, **kwargs):

        goal = Goal.objects.get(pk=request.session['goal_id'])
        if 'active_lesson_id' in request.session:  # Todo decorator is_active_lesson
            lesson = Lesson.objects.get(pk=request.session['active_lesson_id'])
        else:
            name = goal.lessons.count() + 1  # Todo Подумать над именем урока
            lesson = Lesson.objects.create(name=name, goal=goal)
            request.session['active_lesson_id'] = lesson.id

        form = LearningForm()
        return render(request, 'lesson.html', {'form': form, 'lesson': lesson})

    def post(self, request, *args, **kwargs):
        form = LearningForm(request.POST)
        theme = Theme.objects.get(pk=request.session['lesson_theme_id'])
        lesson = Lesson.objects.get(pk=request.session['active_lesson_id'])
        if form.is_valid():
            cd = form.cleaned_data
            question = cd['question']
            answer = cd['answer']
            new_question = Question.objects.create(question=question,
                                                   answer=answer,
                                                   lesson=lesson,
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
