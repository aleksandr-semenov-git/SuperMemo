from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from lesson.views import ChooseThemePage, AddThemePage


class ThemePagesTest(SimpleTestCase):
    FILE_PATH = 'lesson.views.theme'

    @patch(f'{FILE_PATH}.render')
    @patch(f'{FILE_PATH}.ChooseThemeForm')
    @patch(f'{FILE_PATH}.GoalService.get_goal_by_id')
    @patch(f'{FILE_PATH}.SectionService.get_section_by_id')
    def test_get_choose_theme(self, patch_get_section, patch_get_goal, patch_form, patch_render):
        test_goal_id = 1
        test_section_id = 2
        mock_request = MagicMock(session={'goal_id': test_goal_id})
        mock_http_result = MagicMock()
        mock_form = MagicMock()
        mock_goal = MagicMock()
        mock_section = MagicMock()

        patch_render.return_value = mock_http_result
        patch_form.return_value = mock_form
        patch_get_goal.return_value = mock_goal
        patch_get_section.return_value = mock_section

        view = ChooseThemePage(request=mock_request)
        result = view.get(mock_request, test_section_id)

        self.assertEqual(result, mock_http_result)
        patch_render.assert_called_once_with(mock_request, 'choose_theme.html', {'form': mock_form,
                                                                                 'goal': mock_goal,
                                                                                 'section': mock_section})
        patch_get_goal.assert_called_once_with(test_goal_id)
        patch_get_section.assert_called_once_with(test_section_id)
        patch_form.assert_called_once_with(section_id=test_section_id)

    @patch(f'{FILE_PATH}.redirect')
    @patch(f'{FILE_PATH}.ChooseThemeForm')
    @patch(f'{FILE_PATH}.ThemeService.get_theme_by_name_and_section_id')
    def test_post_choose_theme_valid_form(self, patch_get_theme, patch_form, patch_redirect):
        test_goal_id = 1
        test_section_id = 2
        mock_request = MagicMock(session={'goal_id': test_goal_id})
        mock_http_result = MagicMock()
        mock_form = MagicMock()
        mock_theme = MagicMock()

        patch_redirect.return_value = mock_http_result
        patch_form.return_value = mock_form
        cd = {'name': 'test_theme_name'}
        mock_form.is_valid.return_value = True
        mock_form.cleaned_data = cd
        patch_get_theme.return_value = mock_theme

        view = ChooseThemePage(request=mock_request)
        result = view.post(mock_request, test_section_id)

        self.assertEqual(result, mock_http_result)
        patch_redirect.assert_called_once_with('lesson:sure', theme_id=mock_theme.id)
        patch_form.assert_called_once_with(mock_request.POST, section_id=test_section_id)
        mock_form.is_valid.assert_called_once()
        patch_get_theme.assert_called_once_with(name='test_theme_name', section_id=test_section_id)
        self.assertEqual(mock_theme.id, mock_request.session['theme_id'])

    @patch(f'{FILE_PATH}.render')
    @patch(f'{FILE_PATH}.ChooseThemeForm')
    @patch(f'{FILE_PATH}.GoalService.get_goal_by_id')
    @patch(f'{FILE_PATH}.SectionService.get_section_by_id')
    def test_post_choose_theme_invalid_form(self, patch_get_section, patch_get_goal, patch_form, patch_render):
        test_goal_id = 1
        test_section_id = 2
        mock_request = MagicMock(session={'goal_id': test_goal_id})
        mock_http_result = MagicMock()
        mock_form = MagicMock()
        mock_goal = MagicMock()
        mock_section = MagicMock()

        patch_render.return_value = mock_http_result
        patch_form.return_value = mock_form
        patch_get_goal.return_value = mock_goal
        patch_get_section.return_value = mock_section
        mock_form.is_valid.return_value = False

        view = ChooseThemePage(request=mock_request)
        result = view.post(mock_request, test_section_id)

        self.assertEqual(result, mock_http_result)
        patch_form.assert_called_once_with(mock_request.POST, section_id=test_section_id)
        mock_form.is_valid.assert_called_once()
        patch_get_goal.assert_called_once_with(test_goal_id)
        patch_get_section.assert_called_once_with(section_id=test_section_id)
        patch_render.assert_called_once_with(mock_request, 'choose_theme.html', {'form': mock_form,
                                                                                 'goal': mock_goal,
                                                                                 'section': mock_section})

    @patch(f'{FILE_PATH}.render')
    @patch(f'{FILE_PATH}.AddThemeForm')
    def test_get_add_theme(self, patch_form, patch_render):
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_form = MagicMock()

        patch_render.return_value = mock_http_result
        patch_form.return_value = mock_form

        view = AddThemePage(request=mock_request)
        result = view.get(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_form.assert_called_once()
        patch_render.assert_called_once_with(mock_request, 'add_theme.html', {'form': mock_form})

    @patch(f'{FILE_PATH}.render')
    @patch(f'{FILE_PATH}.AddThemeForm')
    @patch(f'{FILE_PATH}.SectionService.get_section_by_id')
    @patch(f'{FILE_PATH}.ThemeService.create_theme')
    def test_post_add_theme_valid_form(self, patch_create_theme, patch_get_section, patch_form, patch_render):
        test_goal_id = 1
        test_section_id = 2
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_form = MagicMock()
        mock_section = MagicMock()
        mock_theme = MagicMock()

        patch_render.return_value = mock_http_result
        patch_form.return_value = mock_form
        patch_get_section.return_value = mock_section
        patch_create_theme.return_value = mock_theme
        cd = {'name': 'testname'}
        mock_form.is_valid.return_value = True
        mock_form.cleaned_data = cd
        patch_create_theme.return_value = mock_theme

        view = AddThemePage(request=mock_request)
        result = view.post(mock_request, test_section_id)

        self.assertEqual(result, mock_http_result)
        patch_render.assert_called_once_with(mock_request, 'add_theme.html', {'form': mock_form})
        patch_form.assert_called_once_with(mock_request.POST)
        patch_get_section.assert_called_once_with(test_section_id)
        mock_form.is_valid.assert_called_once()
        patch_create_theme.assert_called_once_with(name='testname', section=mock_section)

    @patch(f'{FILE_PATH}.redirect')
    @patch(f'{FILE_PATH}.AddThemeForm')
    @patch(f'{FILE_PATH}.SectionService.get_section_by_id')
    def test_post_add_section_invalid_form(self, patch_get_section, patch_form, patch_redirect):
        test_section_id = 2
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_form = MagicMock()
        mock_section = MagicMock()

        patch_redirect.return_value = mock_http_result
        patch_form.return_value = mock_form
        patch_get_section.return_value = mock_section
        mock_form.is_valid.return_value = False

        view = AddThemePage(request=mock_request)
        result = view.post(mock_request, test_section_id)

        self.assertEqual(result, mock_http_result)
        patch_redirect.assert_called_once_with('lesson:choose_theme', section_id=mock_section.id)
        patch_form.assert_called_once_with(mock_request.POST)
        patch_get_section.assert_called_once_with(test_section_id)
        mock_form.is_valid.assert_called_once()
