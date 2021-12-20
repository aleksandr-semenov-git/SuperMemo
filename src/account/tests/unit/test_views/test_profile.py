from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from account.views import ProfilePage, ProfilePageBasic, EditPage


class ProfilePagesTest(SimpleTestCase):
    FILE_PATH = 'account.views.profile'

    @patch(f'{FILE_PATH}.render')
    @patch(f'{FILE_PATH}.GoalService.get_goals_by_profile')
    @patch(f'{FILE_PATH}.ProfileService.get_or_create_profile')
    def test_get_profile_page(self, patch_get_create_profile, patch_get_goals, patch_render):
        username = 'testusername'
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_goals = MagicMock()
        mock_profile = MagicMock()

        patch_render.return_value = mock_http_result
        patch_get_create_profile.return_value = mock_profile
        patch_get_goals.return_value = mock_goals

        view = ProfilePage(request=mock_request)
        result = view.get(mock_request, username=username)

        self.assertEqual(result, mock_http_result)
        patch_render.assert_called_once_with(mock_request, 'profile_page.html', {'profile': mock_profile,
                                                                                 'goals': mock_goals,
                                                                                 'username': username})

    @patch(f'{FILE_PATH}.redirect')
    def test_get_profile_basic_user_is_authenticated(self, patch_redirect):
        mock_request = MagicMock()
        mock_http_result = MagicMock()

        mock_request.user.is_authenticated = True
        patch_redirect.return_value = mock_http_result

        view = ProfilePageBasic(request=mock_request)
        result = view.get(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_redirect.assert_called_once_with('account:profile', username=mock_request.user.username)

    @patch(f'{FILE_PATH}.redirect')
    def test_get_profile_basic_user_is_not_authenticated(self, patch_redirect):
        mock_request = MagicMock()
        mock_http_result = MagicMock()

        mock_request.user.is_authenticated = False
        patch_redirect.return_value = mock_http_result

        view = ProfilePageBasic(request=mock_request)
        result = view.get(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_redirect.assert_called_once_with('account:login')

    @patch(f'{FILE_PATH}.render')
    @patch(f'{FILE_PATH}.PersonalDataEditForm')
    def test_get_edit_page(self, patch_form, patch_render):
        mock_request = MagicMock()
        mock_user = MagicMock()
        mock_request.user = mock_user
        mock_http_result = MagicMock()
        mock_form = MagicMock()

        patch_render.return_value = mock_http_result
        patch_form.return_value = mock_form

        view = EditPage(request=mock_request)
        result = view.get(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_render.assert_called_once_with(mock_request, 'edit.html', {'form': mock_form})
        patch_form.assert_called_once_with(initial={'username': mock_user.username,
                                                    'email': mock_user.email,
                                                    'first_name': mock_user.first_name,
                                                    'last_name': mock_user.last_name})

    @patch(f'{FILE_PATH}.render')
    @patch(f'{FILE_PATH}.PersonalDataEditForm')
    def test_post_edit_page_invalid_form(self, patch_form, patch_render):
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_form = MagicMock()

        patch_render.return_value = mock_http_result
        patch_form.return_value = mock_form
        mock_form.is_valid.return_value = False

        view = EditPage(request=mock_request)
        result = view.post(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_render.assert_called_once_with(mock_request, 'edit.html', {'form': mock_form})
        patch_form.assert_called_once_with(mock_request.POST, instance=mock_request.user)
        mock_form.is_valid.assert_called_once()

    @patch(f'{FILE_PATH}.redirect')
    @patch(f'{FILE_PATH}.PersonalDataEditForm')
    def test_post_edit_page_valid_form(self, patch_form, patch_redirect):
        username = 'testusername'
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_form = MagicMock()

        patch_redirect.return_value = mock_http_result
        patch_form.return_value = mock_form
        mock_form.is_valid.return_value = True
        cd = {'username': username}
        mock_form.cleaned_data = cd

        view = EditPage(request=mock_request)
        result = view.post(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_redirect.assert_called_once_with('account:profile', username='testusername')
        patch_form.assert_called_once_with(mock_request.POST, instance=mock_request.user)
        mock_form.is_valid.assert_called_once()
        mock_form.save.assert_called_once_with(commit=True)
