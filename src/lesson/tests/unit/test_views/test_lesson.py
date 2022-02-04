from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from lesson.views import LessonLearnPage, EditQuestionPage, DeleteQuestionView


class LessonViewsLessonTest(SimpleTestCase):
    FILE_PATH = 'lesson.views.lesson'

    @patch('lesson.views.lesson.render')
    @patch('lesson.views.lesson.LessonService.get_or_create_lesson')
    @patch('lesson.views.lesson.GoalService.get_goal_by_id')
    @patch('lesson.views.lesson.ThemeService.get_theme_by_id')
    @patch('lesson.views.lesson.AddEditQuestionForm')
    def test_get_lesson_learn_page(
            self, patch_form, patch_get_theme, patch_get_goal, patch_get_or_create_lesson, patch_render):
        test_goal_id = 1
        test_theme_id = 2
        mock_request = MagicMock(session={'goal_id': test_goal_id})
        mock_http_result = MagicMock()
        mock_form = MagicMock()
        mock_goal = MagicMock()
        mock_lesson = MagicMock()
        mock_theme = MagicMock()

        patch_render.return_value = mock_http_result
        patch_get_goal.return_value = mock_goal
        patch_get_theme.return_value = mock_theme
        patch_form.return_value = mock_form
        patch_get_or_create_lesson.return_value = mock_lesson

        view = LessonLearnPage(request=mock_request)
        result = view.get(mock_request, test_theme_id)

        self.assertEqual(mock_request.session['goal_id'], test_goal_id)
        self.assertEqual(result, mock_http_result)
        patch_get_goal.assert_called_once_with(test_goal_id)
        patch_get_theme.assert_called_once_with(test_theme_id)
        patch_get_or_create_lesson.assert_called_once_with(goal=mock_goal, theme=mock_theme)
        patch_form.assert_called_once()
        patch_render.assert_called_once_with(mock_request, 'lesson_learn.html', {'form': mock_form,
                                                                                 'lesson': mock_lesson})

    @patch('lesson.views.lesson.redirect')
    @patch('lesson.views.lesson.QuestionService.create_question')
    @patch('lesson.views.lesson.LessonService.get_lesson_by_theme_id')
    @patch('lesson.views.lesson.AddEditQuestionForm')
    @patch('lesson.views.lesson.ThemeService.get_theme_by_id')
    def test_post_lesson_learn_page_invalid_form(
            self, patch_get_theme, patch_form, patch_get_lesson, patch_create_question, patch_redirect):
        test_theme_id = 1
        mock_request = MagicMock(session={'theme_id': test_theme_id})
        mock_http_result = MagicMock()
        mock_form = MagicMock()
        mock_lesson = MagicMock()
        mock_theme = MagicMock()
        mock_theme.id = test_theme_id

        cd = {'question': 'testquestion', 'answer': 'testanswer'}
        patch_form.return_value = mock_form
        patch_get_theme.return_value = mock_theme
        patch_get_lesson.return_value = mock_lesson
        mock_form.cleaned_data = cd
        mock_form.is_valid.return_value = True
        patch_redirect.return_value = mock_http_result

        view = LessonLearnPage(request=mock_request)
        result = view.post(mock_request, test_theme_id)

        self.assertEqual(result, mock_http_result)
        self.assertEqual(mock_request.session['theme_id'], test_theme_id)
        mock_form.is_valid.assert_called_once()
        patch_form.assert_called_once_with(mock_request.POST)
        patch_get_theme.assert_called_once_with(test_theme_id)
        patch_create_question.assert_called_once_with(
            question='testquestion', answer='testanswer', lesson=mock_lesson)
        patch_redirect.assert_called_once_with('lesson:lesson_learn', theme_id=test_theme_id)

    @patch('lesson.views.lesson.render')
    @patch('lesson.views.lesson.LessonService.get_lesson_by_theme_id')
    @patch('lesson.views.lesson.AddEditQuestionForm')
    @patch('lesson.views.lesson.ThemeService.get_theme_by_id')
    def test_post_lesson_learn_page_valid_form(
            self, patch_get_theme, patch_form, patch_get_lesson, patch_render):
        test_theme_id = 1
        mock_request = MagicMock(session={'theme_id': test_theme_id})
        mock_http_result = MagicMock()
        mock_form = MagicMock()
        mock_lesson = MagicMock()
        mock_theme = MagicMock()
        mock_theme.id = test_theme_id

        patch_form.return_value = mock_form
        patch_get_theme.return_value = mock_theme
        patch_get_lesson.return_value = mock_lesson
        mock_form.is_valid.return_value = False
        patch_render.return_value = mock_http_result

        view = LessonLearnPage(request=mock_request)
        result = view.post(mock_request, test_theme_id)

        self.assertEqual(result, mock_http_result)
        self.assertEqual(mock_request.session['theme_id'], test_theme_id)
        patch_form.assert_called_once_with(mock_request.POST)
        patch_get_theme.assert_called_once_with(test_theme_id)
        patch_get_lesson.assert_called_once_with(test_theme_id)
        mock_form.is_valid.assert_called_once()
        patch_render.assert_called_once_with(
            mock_request, 'lesson_learn.html', {'form': mock_form, 'lesson': mock_lesson})

    @patch('lesson.views.lesson.render')
    @patch('lesson.views.lesson.AddEditQuestionForm')
    @patch('lesson.views.lesson.QuestionService.get_question_by_id')
    def test_get_edit_question_page(self, patch_get_question, patch_form, patch_render):
        test_question_id = 1
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_form = MagicMock()
        mock_question = MagicMock(question='testq', answer='testa')
        test_initital = {'question': mock_question.question,
                         'answer': mock_question.answer}

        patch_get_question.return_value = mock_question
        patch_form.return_value = mock_form
        patch_render.return_value = mock_http_result

        view = EditQuestionPage(request=mock_request)
        result = view.get(mock_request, test_question_id)

        self.assertEqual(result, mock_http_result)
        patch_get_question.assert_called_once_with(test_question_id)
        patch_form.assert_called_once_with(initial=test_initital)
        patch_render.assert_called_once_with(
            mock_request, 'edit_question.html', {'form': mock_form, 'question': mock_question})

    @patch('lesson.views.lesson.redirect')
    @patch('lesson.views.lesson.AddEditQuestionForm')
    @patch('lesson.views.lesson.QuestionService.get_question_by_id')
    def test_post_edit_question_page_valid_form(self, patch_get_question, patch_form, patch_redirect):
        test_question_id = 1
        test_theme_id = 2
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_form = MagicMock()
        mock_question = MagicMock(question='testq', answer='testa')
        mock_lesson = MagicMock()

        mock_question.lesson = mock_lesson
        mock_lesson.theme.id = test_theme_id
        patch_get_question.return_value = mock_question
        patch_form.return_value = mock_form
        patch_redirect.return_value = mock_http_result
        mock_form.is_valid.return_value = True

        view = EditQuestionPage(request=mock_request)
        result = view.post(mock_request, test_question_id)

        self.assertEqual(result, mock_http_result)
        patch_get_question.assert_called_once_with(test_question_id)
        patch_form.assert_called_once_with(mock_request.POST, instance=mock_question)
        mock_form.is_valid.assert_called_once()
        mock_form.save.assert_called_once_with(commit=True)
        patch_redirect.assert_called_once_with('lesson:lesson_learn', theme_id=test_theme_id)

    @patch('lesson.views.lesson.render')
    @patch('lesson.views.lesson.AddEditQuestionForm')
    @patch('lesson.views.lesson.QuestionService.get_question_by_id')
    def test_post_edit_question_page_invalid_form(self, patch_get_question, patch_form, patch_render):
        test_question_id = 1
        test_theme_id = 2
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_form = MagicMock()
        mock_question = MagicMock(question='testq', answer='testa')
        mock_lesson = MagicMock()

        mock_question.lesson = mock_lesson
        mock_lesson.theme.id = test_theme_id
        patch_get_question.return_value = mock_question
        patch_form.return_value = mock_form
        patch_render.return_value = mock_http_result
        mock_form.is_valid.return_value = False

        view = EditQuestionPage(request=mock_request)
        result = view.post(mock_request, test_question_id)

        self.assertEqual(result, mock_http_result)
        patch_get_question.assert_called_once_with(test_question_id)
        patch_form.assert_called_once_with(mock_request.POST, instance=mock_question)
        patch_render.assert_called_once_with(
            mock_request, 'lesson_learn.html', {'form': mock_form, 'lesson': mock_lesson})

    @patch('lesson.views.lesson.redirect')
    @patch('lesson.views.lesson.QuestionService.get_question_by_id')
    def test_get_delete_question_view(self, patch_get_question, patch_redirect):
        test_question_id = 1
        test_theme_id = 2
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_question = MagicMock()
        mock_lesson = MagicMock()

        patch_redirect.return_value = mock_http_result
        mock_question.lesson = mock_lesson
        mock_lesson.theme.id = test_theme_id
        patch_get_question.return_value = mock_question

        view = DeleteQuestionView(request=mock_request)
        result = view.get(mock_request, test_question_id)

        self.assertEqual(result, mock_http_result)
        patch_get_question.assert_called_once_with(test_question_id)
        mock_question.delete.assert_called_once()
        patch_redirect.assert_called_once_with('lesson:lesson_learn', theme_id=test_theme_id)
