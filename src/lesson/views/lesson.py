from django.shortcuts import render, redirect
from django.views import View
from memo.models import Lesson, Question, Goal, Theme
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from lesson.forms import LearningForm
from memo.services import GoalService, SectionService, ThemeService
from memo.services.model_service import LessonService, QuestionService


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

        goal = GoalService.get_goal_by_id(request.session['goal_id'])
        if 'active_lesson_id' in request.session:  # Todo decorator is_active_lesson
            lesson = LessonService.get_lesson_by_id(request.session['active_lesson_id'])
        else:
            name = goal.lessons.count() + 1  # Todo Think about lesson_name
            lesson = LessonService.create_lesson(name=name, goal=goal)
            request.session['active_lesson_id'] = lesson.id

        form = LearningForm()
        return render(request, 'lesson.html', {'form': form, 'lesson': lesson})

    def post(self, request, *args, **kwargs):
        form = LearningForm(request.POST)
        theme = ThemeService.get_theme_by_id(request.session['lesson_theme_id'])
        lesson = LessonService.get_lesson_by_id(request.session['active_lesson_id'])
        if form.is_valid():
            cd = form.cleaned_data
            question = cd['question']
            answer = cd['answer']
            QuestionService.create_question(question=question,
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
        lesson = LessonService.get_lesson_by_id(request.session['active_lesson_id'])
        return render(request, 'end_lesson.html', {'lesson': lesson})

    def post(self, request, *args, **kwargs):
        if request.POST.get('end') == 'End lesson':
            goal = GoalService.get_goal_by_id(request.session['goal_id'])
            request.session.pop('active_lesson_id')
            request.session.pop('lesson_section_id')
            request.session.pop('lesson_theme_id')
            return redirect('memo:goal_page', goal_id=goal.id)
        else:
            return redirect('lesson:lesson_page')
