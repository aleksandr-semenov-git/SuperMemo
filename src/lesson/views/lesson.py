from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from lesson.forms import AddEditQuestionForm
from lesson.services import LessonService, ThemeService, QuestionService
from memo.services import GoalService


@method_decorator(login_required, name='dispatch')
class LessonLearnPage(View):
    def get(self, request, theme_id, *args, **kwargs):
        """Render page. User see LearningForm and table with questions and answers.

        User can edit or delete questions. User see logout, repeat-theme, back-to-<goal>, back-to-profile,
        back-to-my-goals buttons.
        """
        goal = GoalService.get_goal_by_id(request.session['goal_id'])
        theme = ThemeService.get_theme_by_id(theme_id)
        lesson = LessonService.get_or_create_lesson(goal=goal, theme=theme)
        form = AddEditQuestionForm()
        return render(request, 'lesson_learn.html', {'form': form, 'lesson': lesson})

    def post(self, request, theme_id, *args, **kwargs):
        """Check data from LearningForm. Render lesson-page again. Show form errors if needed"""
        form = AddEditQuestionForm(request.POST)
        theme = ThemeService.get_theme_by_id(theme_id)
        theme_id = theme.id
        lesson = LessonService.get_lesson_by_theme_id(theme_id)
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


@method_decorator(login_required, name='dispatch')
class EditQuestionPage(View):
    """Render page. User see question, answer, AddEditQuestionForm, logout and save-question buttons"""
    def get(self, request, question_id, *args, **kwargs):
        question = QuestionService.get_question_by_id(question_id)
        form = AddEditQuestionForm(initial={'question': question.question,
                                            'answer': question.answer})
        return render(request, 'edit_question.html', {'form': form, 'question': question})

    def post(self, request, question_id):
        """Check data from AddEditQuestionForm. Render lesson-page. Show form errors if needed."""
        question = QuestionService.get_question_by_id(question_id)
        form = AddEditQuestionForm(request.POST, instance=question)
        lesson = question.lesson
        theme_id = lesson.theme.id
        if form.is_valid():
            form.save(commit=True)
            return redirect('lesson:lesson_learn', theme_id=theme_id)
        else:
            return render(request, 'lesson_learn.html', {'form': form, 'lesson': lesson})


@method_decorator(login_required, name='dispatch')
class DeleteQuestionView(View):
    def get(self, request, question_id, *args, **kwargs):
        """Delete chosen Question object by id. Render lesson-page again"""
        question = QuestionService.get_question_by_id(question_id)
        lesson = question.lesson
        theme_id = lesson.theme.id
        question.delete()
        return redirect('lesson:lesson_learn', theme_id=theme_id)
