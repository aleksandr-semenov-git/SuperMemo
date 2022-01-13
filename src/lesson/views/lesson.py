from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from lesson.forms import LearningForm
from lesson.models import Theme
from memo.services import GoalService
from lesson.services.model_service import SectionService, ThemeService, LessonService, QuestionService


@method_decorator(login_required, name='dispatch')
class LessonPage(View):
    def get(self, request, theme_id, *args, **kwargs):
        """Render lesson-page and LearningForm"""
        goal = GoalService.get_goal_by_id(request.session['goal_id'])
        theme = Theme.objects.get(pk=theme_id)
        section_name = theme.section.name
        theme_name = theme.name

        name = f'{goal.name} {section_name} {theme_name}'
        lesson = LessonService.get_or_create_lesson(name=name, goal=goal, theme=theme)
        request.session['active_lesson_id'] = lesson.id

        form = LearningForm()
        return render(request, 'lesson.html', {'form': form, 'lesson': lesson})

    def post(self, request, *args, **kwargs):
        """Gather and check data from learning-form. Render lesson-page again

        Control active-lesson by django-sessions with theme_id, active_lesson_id keys
        """
        form = LearningForm(request.POST)
        theme = ThemeService.get_theme_by_id(request.session['theme_id'])
        lesson = LessonService.get_lesson_by_id(request.session['active_lesson_id'])
        if form.is_valid():
            cd = form.cleaned_data
            question = cd['question']
            answer = cd['answer']
            QuestionService.create_question(question=question,
                                            answer=answer,
                                            lesson=lesson,
                                            theme=theme)
            return redirect('lesson:lesson_page')
        else:
            return render(request, 'lesson.html', {'form': form, 'lesson': lesson})
