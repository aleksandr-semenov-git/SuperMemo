from unittest.mock import patch, MagicMock
from django.test import TestCase
from lesson.views import MyLessonsPage, SurePage, LessonPage


class LessonPagesTest(TestCase):
    @patch('lesson.views.lesson.render')
    @patch('lesson.views.lesson.LessonService.get_lessons_by_profile')
    def test_get_mylessons_page(self, patch_get_lessons, patch_render):
        mock_request = MagicMock()
        mock_render_result = MagicMock()
        mock_profile = MagicMock()
        mock_request.user.profile = mock_profile
        mock_lessons = MagicMock()

        patch_render.return_value = mock_render_result
        patch_get_lessons.return_value = mock_lessons

        view = MyLessonsPage(request=mock_request)
        result = view.get(mock_request)

        self.assertEqual(result, mock_render_result)
        patch_get_lessons.assert_called_once_with(profile=mock_profile)
        patch_render.assert_called_once_with(mock_request, 'my_lessons.html', {'lessons': mock_lessons})

    @patch('lesson.views.lesson.render')
    @patch('lesson.services.model_service.LessonService.get_lesson_by_id')
    @patch('memo.services.model_service.GoalService.get_goal_by_id')
    @patch('lesson.views.lesson.LearningForm')
    def test_get_lesson_page_lesson_id_in_session(self, patch_form, patch_get_goal, patch_get_lesson, patch_render):
        test_goal_id = 1
        active_lesson_id = 1
        mock_request = MagicMock(session={'goal_id': test_goal_id, 'active_lesson_id': active_lesson_id})
        mock_render_result = MagicMock()
        mock_form = MagicMock()
        mock_goal = MagicMock()
        mock_lesson = MagicMock()

        patch_get_goal.return_value = mock_goal
        patch_form.return_value = mock_form
        patch_render.return_value = mock_render_result
        patch_get_lesson.return_value = mock_lesson

        view = LessonPage(request=mock_request)
        result = view.get(mock_request)

        self.assertEqual(mock_request.session['goal_id'], test_goal_id)
        self.assertEqual(result, mock_render_result)
        patch_get_goal.assert_called_once_with(test_goal_id)
        patch_get_lesson.assert_called_once_with(active_lesson_id)
        patch_render.assert_called_once_with(mock_request, 'lesson.html', {'form': mock_form, 'lesson': mock_lesson})

    @patch('lesson.views.lesson.render')
    @patch('lesson.services.model_service.LessonService.create_lesson')
    @patch('memo.services.model_service.GoalService.get_goal_by_id')
    @patch('lesson.views.lesson.LearningForm')
    def test_get_lesson_page_else(
            self, patch_form, patch_get_goal, patch_create_lesson, patch_render):
        test_goal_id = 1
        mock_request = MagicMock(session={'goal_id': test_goal_id})
        mock_render_result = MagicMock()
        mock_form = MagicMock()
        mock_goal = MagicMock()
        mock_lesson = MagicMock()

        patch_get_goal.return_value = mock_goal
        test_lesson_name = 1
        mock_goal.lessons.return_value = test_lesson_name
        mock_goal.lessons.count.return_value = test_lesson_name
        patch_form.return_value = mock_form
        patch_render.return_value = mock_render_result
        patch_create_lesson.return_value = mock_lesson

        mock_goal.reset_mock()
        view = LessonPage(request=mock_request)
        result = view.get(mock_request)

        self.assertEqual(result, mock_render_result)
        patch_get_goal.assert_called_once_with(test_goal_id)
        self.assertEqual(mock_request.session['goal_id'], test_goal_id)
        mock_goal.lessons.count.assert_called_once()
        patch_create_lesson.assert_called_once_with(name=test_lesson_name + 1, goal=mock_goal)
        self.assertEqual(mock_request.session['active_lesson_id'], mock_lesson.id)
        patch_render.assert_called_once_with(mock_request, 'lesson.html', {'form': mock_form, 'lesson': mock_lesson})

    @patch('lesson.views.lesson.render')
    @patch('lesson.services.model_service.QuestionService.create_question')
    @patch('lesson.services.model_service.LessonService.get_lesson_by_id')
    @patch('lesson.views.lesson.LearningForm')
    @patch('lesson.services.model_service.ThemeService.get_theme_by_id')
    def test_post_lesson_page_valid_form(
            self, patch_get_theme, patch_form, patch_get_lesson, patch_create_question, patch_render):
        test_theme_id = 1
        test_active_lesson_id = 1
        mock_request = MagicMock(session={'theme_id': test_theme_id, 'active_lesson_id': test_active_lesson_id})
        mock_render_result = MagicMock()
        mock_form = MagicMock()
        mock_lesson = MagicMock()
        mock_theme = MagicMock()

        cd = {'question': 'testquestion', 'answer': 'testanswer'}
        patch_form.return_value = mock_form
        patch_get_theme.return_value = mock_theme
        patch_get_lesson.return_value = mock_lesson
        mock_form.cleaned_data = cd
        mock_form.is_valid.return_value = True
        patch_render.return_value = mock_render_result

        patch_form.reset_mock()
        view = LessonPage(request=mock_request)
        result = view.post(mock_request)

        self.assertEqual(result, mock_render_result)
        self.assertEqual(mock_request.session['theme_id'], test_theme_id)
        self.assertEqual(mock_request.session['active_lesson_id'], test_active_lesson_id)
        mock_form.is_valid.assert_called_once()

        # patch_form.assert_called_with(mock_request.POST)  # Todo: fix
        patch_get_theme.assert_called_once_with(test_theme_id)
        patch_get_lesson.assert_called_once_with(test_active_lesson_id)
        patch_create_question.assert_called_once_with(
            question='testquestion', answer='testanswer', lesson=mock_lesson, theme=mock_theme)
        patch_render.assert_called_once_with(mock_request, 'lesson.html', {'form': mock_form, 'lesson': mock_lesson})

    @patch('lesson.views.lesson.render')
    @patch('lesson.services.model_service.LessonService.get_lesson_by_id')
    @patch('lesson.views.lesson.LearningForm')
    @patch('lesson.services.model_service.ThemeService.get_theme_by_id')
    def test_post_lesson_page_invalid_form(
            self, patch_get_theme, patch_form, patch_get_lesson, patch_render):
        test_theme_id = 1
        test_active_lesson_id = 1
        mock_request = MagicMock(session={'theme_id': test_theme_id, 'active_lesson_id': test_active_lesson_id})
        mock_render_result = MagicMock()
        mock_form = MagicMock()
        mock_lesson = MagicMock()
        mock_theme = MagicMock()

        patch_get_theme.return_value = mock_theme
        patch_get_lesson.return_value = mock_lesson
        patch_form.return_value = mock_form
        patch_get_lesson.return_value = mock_lesson
        mock_form.is_valid.return_value = False
        patch_render.return_value = mock_render_result

        patch_form.reset_mock()
        view = LessonPage(request=mock_request)
        result = view.post(mock_request)

        self.assertEqual(result, mock_render_result)
        self.assertEqual(mock_request.session['theme_id'], test_theme_id)
        self.assertEqual(mock_request.session['active_lesson_id'], test_active_lesson_id)
        mock_form.is_valid.assert_called_once()

        patch_get_theme.assert_called_once_with(test_theme_id)
        patch_get_lesson.assert_called_once_with(test_active_lesson_id)
        patch_render.assert_called_once_with(mock_request, 'lesson.html', {'form': mock_form, 'lesson': mock_lesson})
        patch_form.assert_called_once_with(mock_request.POST)
