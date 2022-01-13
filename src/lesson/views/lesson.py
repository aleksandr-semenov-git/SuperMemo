from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from lesson.forms import LearningForm
from lesson.models import Theme, Lesson
from memo.services import GoalService
from lesson.services.model_service import SectionService, ThemeService, LessonService, QuestionService


@method_decorator(login_required, name='dispatch')
class LessonLearnPage(View):
    def get(self, request, theme_id, *args, **kwargs):
        """Render lesson-page and LearningForm"""
        request.session['theme_id'] = theme_id
        goal = GoalService.get_goal_by_id(request.session['goal_id'])
        theme = Theme.objects.get(pk=theme_id)
        section_name = theme.section.name
        theme_name = theme.name

        name = f'{goal.name} {section_name} {theme_name}'
        lesson = LessonService.get_or_create_lesson(name=name, goal=goal, theme=theme)

        form = LearningForm()
        return render(request, 'lesson_learn.html', {'form': form, 'lesson': lesson})

    def post(self, request, theme_id, *args, **kwargs):
        """Gather and check data from learning-form. Render lesson-page again

        Control active-lesson by django-sessions with theme_id, active_lesson_id keys
        """
        form = LearningForm(request.POST)
        theme = ThemeService.get_theme_by_id(request.session['theme_id'])
        lesson = Lesson.objects.get(theme__id=theme.id)
        if form.is_valid():
            cd = form.cleaned_data
            question = cd['question']
            answer = cd['answer']
            QuestionService.create_question(question=question,
                                            answer=answer,
                                            lesson=lesson,
                                            )
            return redirect('lesson:lesson_learn', theme_id=theme_id)
        else:
            return render(request, 'lesson_learn.html', {'form': form, 'lesson': lesson})
