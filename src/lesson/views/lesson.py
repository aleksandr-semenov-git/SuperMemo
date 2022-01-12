from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from lesson.forms import LearningForm
from lesson.models import Theme
from memo.services import GoalService
from lesson.services.model_service import SectionService, ThemeService, LessonService, QuestionService


@method_decorator(login_required, name='dispatch')
class MyLessonsPage(View):
    """Render my-lessons-page with list of user's lessons"""
    def get(self, request, *args, **kwargs):
        lessons = LessonService.get_lessons_by_profile(profile=request.user.profile)
        return render(request, 'my_lessons.html', {'lessons': lessons})


@method_decorator(login_required, name='dispatch')
class SurePage(View):
    def get(self, request, theme_id, *args, **kwargs):
        """Render confirm-page

        User confirm information about the lesson: goal, section, theme
        Control active-lesson by django-sessions with goal_id, theme_id keys
        """
        theme = ThemeService.get_theme_by_id(theme_id)
        request.session['theme_id'] = theme.id
        section = SectionService.get_section_by_id(theme.section.id)
        goal = GoalService.get_goal_by_id(request.session['goal_id'])
        return render(request, 'sure_page.html', {'goal': goal, 'section': section, 'theme': theme})

    def post(self, request, *args, **kwargs):
        """Redirect to the lesson_page after confirmation"""
        return redirect('lesson:lesson_page')


@method_decorator(login_required, name='dispatch')
class LessonPage(View):
    def get(self, request, *args, **kwargs):
        """Render lesson-page and LearningForm

        Control active-lesson by django-sessions with goal_id, active_lesson_id keys
        Check if active-lesson exists. If active-lesson not exist view will create it and save it's id in session
        """
        if 'active_lesson_id' in request.session:  # Todo decorator is_active_lesson
            lesson = LessonService.get_lesson_by_id(request.session['active_lesson_id'])
        else:
            goal = GoalService.get_goal_by_id(request.session['goal_id'])
            section_name = Theme.objects.get(pk=request.session['theme_id']).section.name
            theme_name = Theme.objects.get(pk=request.session['theme_id']).name
            lesson = LessonService.create_lesson(name='', goal=goal)
            name = f'{goal.name} {section_name} {theme_name} {lesson.start.strftime("%Y-%m-%d")}'
            lesson.__setattr__('name', name)
            lesson.save()
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


@method_decorator(login_required, name='dispatch')
class EndLessonPage(View):
    def get(self, request, *args, **kwargs):
        """Render end-lesson page. User confirm to end lesson or continue it

        Control active-lesson by django-sessions with theme_id, active_lesson_id keys
        """
        lesson = LessonService.get_lesson_by_id(request.session['active_lesson_id'])
        return render(request, 'end_lesson.html', {'lesson': lesson})

    def post(self, request, *args, **kwargs):
        """Listen user's answer and redirect to goal-page or just redirect back to lesson-page

        If user end lesson:
        Get lesson's goal to redirect user to goal-page
        Delete active-lesson's keys: active_lesson_id, theme_id
        Redirect to the goal-page
        Else: redirect back to the active-lesson
        """
        if request.POST.get('end') == 'End lesson':
            goal = GoalService.get_goal_by_id(request.session['goal_id'])
            request.session.pop('active_lesson_id')
            request.session.pop('theme_id')
            return redirect('memo:goal_page', goal_id=goal.id)
        else:
            return redirect('lesson:lesson_page')
