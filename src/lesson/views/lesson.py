from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from lesson.forms import LearningForm
from memo.services import GoalService, SectionService, ThemeService
from memo.services.model_service import LessonService, QuestionService


@method_decorator(login_required, name='dispatch')
class MyLessonsPage(View):
    """Render my-lessons-page with list of user's lessons"""
    def get(self, request, *args, **kwargs):
        lessons = LessonService.get_lessons_by_profile(profile=request.user.profile)
        return render(request, 'my_lessons.html', {'lessons': lessons})


@method_decorator(login_required, name='dispatch')
class SurePage(View):
    def get(self, request, *args, **kwargs):
        """Render confirm-page

        User confirm information about the lesson: goal, section, theme
        View get theme_id key from kwargs
        Control active-lesson by django-sessions with goal_id, theme_id keys
        """
        theme = ThemeService.get_theme_by_id(theme_id=kwargs['theme_id'])
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
        goal = GoalService.get_goal_by_id(request.session['goal_id'])
        if 'active_lesson_id' in request.session:  # Todo decorator is_active_lesson
            lesson = LessonService.get_lesson_by_id(request.session['active_lesson_id'])
        else:
            name = goal.lessons.count() + 1
            lesson = LessonService.create_lesson(name=name, goal=goal)
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
            form = LearningForm()
            return render(request, 'lesson.html', {'form': form, 'lesson': lesson})
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
