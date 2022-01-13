from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from lesson.views import MyLessonsPage, SurePage, LessonLearnPage, EndLessonPage


class LessonPagesTest(SimpleTestCase):
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
    @patch('lesson.views.lesson.LessonService.get_lesson_by_id')
    @patch('lesson.views.lesson.GoalService.get_goal_by_id')
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

        view = LessonLearnPage(request=mock_request)
        result = view.get(mock_request)

        self.assertEqual(mock_request.session['goal_id'], test_goal_id)
        self.assertEqual(result, mock_render_result)
        patch_get_lesson.assert_called_once_with(active_lesson_id)
        patch_render.assert_called_once_with(mock_request, 'lesson_learn.html', {'form': mock_form, 'lesson': mock_lesson})

    @patch('lesson.views.lesson.render')
    @patch('lesson.views.lesson.LessonService.create_lesson')
    @patch('lesson.views.lesson.GoalService.get_goal_by_id')
    @patch('lesson.views.lesson.LearningForm')
    @patch('lesson.views.lesson.Theme.objects.get')
    def test_get_lesson_page_else(
            self, patch_get_theme, patch_form, patch_get_goal, patch_create_lesson, patch_render):
        test_goal_id = 1
        test_theme_id = 2
        test_section_name = 'test_section_name'
        mock_request = MagicMock(session={'goal_id': test_goal_id, 'theme_id': test_theme_id})
        mock_render_result = MagicMock()
        mock_form = MagicMock()
        mock_goal = MagicMock()
        mock_lesson = MagicMock()
        mock_theme = MagicMock()
        mock_goal.name = 'test_goal_name'

        mock_theme.section.name = test_section_name
        patch_get_goal.return_value = mock_goal
        mock_goal.lessons.count.return_value = 2
        patch_form.return_value = mock_form
        patch_render.return_value = mock_render_result
        patch_create_lesson.return_value = mock_lesson
        patch_get_theme.return_value = mock_theme

        mock_goal.reset_mock()
        view = LessonLearnPage(request=mock_request)
        result = view.get(mock_request)

        self.assertEqual(result, mock_render_result)
        patch_get_goal.assert_called_once_with(test_goal_id)
        self.assertEqual(mock_request.session['goal_id'], test_goal_id)
        patch_create_lesson.assert_called_once_with(name='', goal=mock_goal)
        self.assertEqual(mock_request.session['active_lesson_id'], mock_lesson.id)
        patch_render.assert_called_once_with(mock_request, 'lesson_learn.html', {'form': mock_form, 'lesson': mock_lesson})

    @patch('lesson.views.lesson.redirect')
    @patch('lesson.views.lesson.QuestionService.create_question')
    @patch('lesson.views.lesson.LessonService.get_lesson_by_id')
    @patch('lesson.views.lesson.LearningForm')
    @patch('lesson.views.lesson.ThemeService.get_theme_by_id')
    def test_post_lesson_page_valid_form(
            self, patch_get_theme, patch_form, patch_get_lesson, patch_create_question, patch_redirect):
        test_theme_id = 1
        test_active_lesson_id = 1
        mock_request = MagicMock(session={'theme_id': test_theme_id, 'active_lesson_id': test_active_lesson_id})
        mock_redirect_result = MagicMock()
        mock_form = MagicMock()
        mock_lesson = MagicMock()
        mock_theme = MagicMock()

        cd = {'question': 'testquestion', 'answer': 'testanswer'}
        patch_form.return_value = mock_form
        patch_get_theme.return_value = mock_theme
        patch_get_lesson.return_value = mock_lesson
        mock_form.cleaned_data = cd
        mock_form.is_valid.return_value = True
        patch_redirect.return_value = mock_redirect_result

        patch_form.reset_mock()
        view = LessonLearnPage(request=mock_request)
        result = view.post(mock_request)

        self.assertEqual(result, mock_redirect_result)
        self.assertEqual(mock_request.session['theme_id'], test_theme_id)
        self.assertEqual(mock_request.session['active_lesson_id'], test_active_lesson_id)
        mock_form.is_valid.assert_called_once()

        patch_form.assert_called_with(mock_request.POST)
        patch_get_theme.assert_called_once_with(test_theme_id)
        patch_get_lesson.assert_called_once_with(test_active_lesson_id)
        patch_create_question.assert_called_once_with(
            question='testquestion', answer='testanswer', lesson=mock_lesson, theme=mock_theme)
        patch_redirect.assert_called_once_with('lesson:lesson_page')

    @patch('lesson.views.lesson.render')
    @patch('lesson.views.lesson.LessonService.get_lesson_by_id')
    @patch('lesson.views.lesson.LearningForm')
    @patch('lesson.views.lesson.ThemeService.get_theme_by_id')
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
        view = LessonLearnPage(request=mock_request)
        result = view.post(mock_request)

        self.assertEqual(result, mock_render_result)
        self.assertEqual(mock_request.session['theme_id'], test_theme_id)
        self.assertEqual(mock_request.session['active_lesson_id'], test_active_lesson_id)
        mock_form.is_valid.assert_called_once()

        patch_get_theme.assert_called_once_with(test_theme_id)
        patch_get_lesson.assert_called_once_with(test_active_lesson_id)
        patch_render.assert_called_once_with(mock_request, 'lesson_learn.html', {'form': mock_form, 'lesson': mock_lesson})
        patch_form.assert_called_once_with(mock_request.POST)

    @patch('lesson.views.lesson.render')
    @patch('lesson.views.lesson.GoalService.get_goal_by_id')
    @patch('lesson.views.lesson.SectionService.get_section_by_id')
    @patch('lesson.views.lesson.ThemeService.get_theme_by_id')
    def test_get_sure_page(self, patch_get_theme, patch_get_section, patch_get_goal, patch_render):
        test_goal_id = 1
        test_theme_id1 = 1
        test_theme_id2 = 2
        test_section_id = 1
        mock_request = MagicMock(session={'goal_id': test_goal_id})
        mock_render_result = MagicMock()
        mock_goal = MagicMock()
        mock_section = MagicMock()
        mock_theme = MagicMock()

        patch_render.return_value = mock_render_result
        patch_get_goal.return_value = mock_goal
        patch_get_section.return_value = mock_section
        patch_get_theme.return_value = mock_theme
        mock_theme.id = test_theme_id2
        mock_theme.section.id = test_section_id

        view = SurePage(request=mock_request)
        result = view.get(mock_request, test_theme_id1)

        self.assertEqual(result, mock_render_result)
        self.assertEqual(mock_request.session['goal_id'], test_goal_id)
        patch_get_theme.assert_called_once_with(test_theme_id1)
        self.assertEqual(mock_request.session['theme_id'], test_theme_id2)
        patch_get_section.assert_called_once_with(test_section_id)
        patch_get_goal.assert_called_once_with(test_goal_id)
        patch_render.assert_called_once_with(
            mock_request, 'sure_page.html', {'goal': mock_goal,
                                             'section': mock_section,
                                             'theme': mock_theme})

    @patch('lesson.views.lesson.redirect')
    def test_post_sure_page(self, patch_redirect):
        mock_request = MagicMock()
        mock_redirect_result = MagicMock()

        patch_redirect.return_value = mock_redirect_result

        view = SurePage(request=mock_request)
        result = view.post(mock_request)

        self.assertEqual(result, mock_redirect_result)
        patch_redirect.assert_called_once_with('lesson:lesson_page')

    @patch('lesson.views.lesson.render')
    @patch('lesson.views.lesson.LessonService.get_lesson_by_id')
    def test_get_end_lesson_page(self, patch_get_lesson, patch_render):
        test_active_lesson_id = 1
        mock_request = MagicMock(session={'active_lesson_id': test_active_lesson_id})
        mock_lesson = MagicMock()
        mock_render_result = MagicMock()

        patch_get_lesson.return_value = mock_lesson
        patch_render.return_value = mock_render_result

        view = EndLessonPage(request=mock_request)
        result = view.get(mock_request)

        self.assertEqual(result, mock_render_result)
        patch_get_lesson.assert_called_once_with(test_active_lesson_id)
        patch_render.assert_called_once_with(mock_request, 'end_lesson.html', {'lesson': mock_lesson})

    @patch('lesson.views.lesson.redirect')
    @patch('lesson.views.lesson.LessonService.get_lesson_by_id')
    @patch('lesson.views.lesson.GoalService.get_goal_by_id')
    def test_post_end_lesson_page_if_end(self, patch_get_goal, patch_get_lesson, patch_redirect):
        test_active_lesson_id = 1
        test_theme_id = 1
        test_goal_id = 1
        mock_request = MagicMock(session={'theme_id': test_theme_id,
                                          'active_lesson_id': test_active_lesson_id,
                                          'goal_id': test_goal_id})
        mock_redirect_result = MagicMock()
        mock_goal = MagicMock()

        mock_request.POST.get.return_value = 'End lesson'
        patch_redirect.return_value = mock_redirect_result
        patch_get_goal.return_value = mock_goal

        view = EndLessonPage(request=mock_request)
        result = view.post(mock_request)

        self.assertEqual(result, mock_redirect_result)
        mock_request.POST.get.assert_called_once_with('end')
        patch_get_goal.assert_called_once_with(test_goal_id)
        self.assertFalse('theme_id' in mock_request.session)
        patch_redirect.assert_called_once_with('memo:goal_page', goal_id=mock_goal.id)

    @patch('lesson.views.lesson.redirect')
    def test_post_end_lesson_page_else(self, patch_redirect):
        mock_request = MagicMock()
        mock_redirect_result = MagicMock()

        patch_redirect.return_value = mock_redirect_result
        mock_request.POST.get.return_value = 'Else'

        view = EndLessonPage(request=mock_request)
        result = view.post(mock_request)

        patch_redirect.assert_called_once_with('lesson:lesson_page')
        self.assertEqual(result, mock_redirect_result)
