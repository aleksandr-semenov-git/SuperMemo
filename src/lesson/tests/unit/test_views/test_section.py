from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase

from lesson.views import AddSectionPage


class SectionPagesTest(SimpleTestCase):
    FILE_PATH = 'lesson.views.section'

    @patch(f'{FILE_PATH}.render')
    @patch(f'{FILE_PATH}.AddSectionForm')
    def test_get_add_section(self, patch_form, patch_render):
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_form = MagicMock()

        patch_render.return_value = mock_http_result
        patch_form.return_value = mock_form

        view = AddSectionPage(request=mock_request)
        result = view.get(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_form.assert_called_once()
        patch_render.assert_called_once_with(mock_request, 'add_section.html', {'form': mock_form})

    @patch(f'{FILE_PATH}.redirect')
    @patch(f'{FILE_PATH}.AddSectionForm')
    @patch(f'{FILE_PATH}.GoalService.get_goal_by_id')
    @patch(f'{FILE_PATH}.SectionService.create_section')
    def test_post_add_section_valid_form(self, patch_create_section, patch_get_goal, patch_form, patch_redirect):
        test_goal_id = 1
        mock_request = MagicMock(session={'goal_id': test_goal_id})
        mock_http_result = MagicMock()
        mock_form = MagicMock()
        mock_goal = MagicMock()
        mock_section = MagicMock()

        patch_redirect.return_value = mock_http_result
        patch_form.return_value = mock_form
        patch_get_goal.return_value = mock_goal
        cd = {'name': 'testname'}
        mock_form.is_valid.return_value = True
        mock_form.cleaned_data = cd
        patch_create_section.return_value = mock_section

        view = AddSectionPage(request=mock_request)
        result = view.post(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_redirect.assert_called_once_with('memo:goal_page', goal_id=test_goal_id)
        patch_form.assert_called_once_with(mock_request.POST)
        patch_get_goal.assert_called_once_with(test_goal_id)
        patch_create_section.assert_called_once_with(name='testname', goal=mock_goal)
        mock_form.is_valid.assert_called_once()

    @patch(f'{FILE_PATH}.render')
    @patch(f'{FILE_PATH}.AddSectionForm')
    def test_post_add_section_invalid_form(self, patch_form, patch_render):
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_form = MagicMock()

        patch_render.return_value = mock_http_result
        patch_form.return_value = mock_form
        mock_form.is_valid.return_value = False

        view = AddSectionPage(request=mock_request)
        result = view.post(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_render.assert_called_once_with(mock_request, 'add_section.html', {'form': mock_form})
        patch_form.assert_called_once_with(mock_request.POST)
        mock_form.is_valid.assert_called_once()
