from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from account.views import LoginView, RegistrationView, LogoutView


class AccountPagesTest(SimpleTestCase):
    FILE_PATH = 'account.views.login_register'

    @patch(f'{FILE_PATH}.render')
    @patch(f'{FILE_PATH}.LoginForm')
    def test_get_login_page(self, patch_form, patch_render):
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_form = MagicMock()

        patch_render.return_value = mock_http_result
        patch_form.return_value = mock_form

        view = LoginView(request=mock_request)
        result = view.get(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_form.assert_called_once()
        patch_render.assert_called_once_with(mock_request, 'login.html', {'form': mock_form})

    @patch(f'{FILE_PATH}.render')
    @patch(f'{FILE_PATH}.LoginForm')
    def test_post_login_page_invalid_form(self, patch_form, patch_render):
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_form = MagicMock()

        patch_render.return_value = mock_http_result
        patch_form.return_value = mock_form
        mock_form.is_valid.return_value = False

        view = LoginView(request=mock_request)
        result = view.post(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_form.assert_called_once()
        mock_form.is_valid.assert_called_once()
        patch_render.assert_called_once_with(mock_request, 'login.html', {'form': mock_form})

    @patch(f'{FILE_PATH}.HttpResponse')
    @patch(f'{FILE_PATH}.LoginForm')
    @patch(f'{FILE_PATH}.authenticate')
    def test_post_login_page_valid_form_user_is_none(self, patch_authenticate, patch_form, patch_httpresponce):
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_form = MagicMock()

        patch_httpresponce.return_value = mock_http_result
        patch_form.return_value = mock_form
        mock_form.is_valid.return_value = True
        cd = {'username': 'username1', 'password': 'password1'}
        mock_form.cleaned_data = cd
        patch_authenticate.return_value = None

        view = LoginView(request=mock_request)
        result = view.post(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_form.assert_called_once_with(mock_request.POST)
        mock_form.is_valid.assert_called_once()
        patch_authenticate.assert_called_once_with(username='username1', password='password1')
        patch_httpresponce.assert_called_once_with('Account with login username1 disabled')

    @patch(f'{FILE_PATH}.redirect')
    @patch(f'{FILE_PATH}.LoginForm')
    @patch(f'{FILE_PATH}.authenticate')
    @patch(f'{FILE_PATH}.login')
    def test_post_login_page_valid_form_user_is_active(
            self, patch_login, patch_authenticate, patch_form, patch_redirect):
        mock_request = MagicMock(session={})
        mock_http_result = MagicMock()
        mock_form = MagicMock()
        mock_user = MagicMock()
        mock_login = MagicMock()

        patch_redirect.return_value = mock_http_result
        patch_form.return_value = mock_form
        mock_form.is_valid.return_value = True
        cd = {'username': 'username1', 'password': 'password1'}
        mock_form.cleaned_data = cd
        patch_authenticate.return_value = mock_user
        mock_user.is_active = True
        patch_login.return_value = mock_login

        view = LoginView(request=mock_request)
        result = view.post(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_redirect.assert_called_once_with('account:profile', username='username1')
        patch_form.assert_called_once_with(mock_request.POST)
        mock_form.is_valid.assert_called_once()
        patch_authenticate.assert_called_once_with(username='username1', password='password1')
        self.assertEqual(mock_request.session['user_id'], mock_user.id)

    @patch(f'{FILE_PATH}.redirect')
    @patch(f'{FILE_PATH}.logout')
    def test_get_logout_view(self, patch_logout, patch_redirect):
        mock_request = MagicMock(session={})
        mock_http_result = MagicMock()

        patch_redirect.return_value = mock_http_result

        view = LogoutView(request=mock_request)
        result = view.get(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_redirect.assert_called_once_with('memo:home')
        patch_logout.assert_called_once_with(mock_request)

    @patch(f'{FILE_PATH}.render')
    @patch(f'{FILE_PATH}.RegistrationForm')
    def test_get_registration_page(self, patch_form, patch_render):
        mock_request = MagicMock(session={})
        mock_http_result = MagicMock()
        mock_form = MagicMock()

        patch_render.return_value = mock_http_result
        patch_form.return_value = mock_form

        view = RegistrationView(request=mock_request)
        result = view.get(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_render.assert_called_once_with(mock_request, 'registration/registration.html', {'form': mock_form})
        patch_form.assert_called_once()

    @patch(f'{FILE_PATH}.render')
    @patch(f'{FILE_PATH}.RegistrationForm')
    def test_get_registration_page_not_valid_form(self, patch_form, patch_render):
        mock_request = MagicMock(session={})
        mock_http_result = MagicMock()
        mock_form = MagicMock()

        patch_render.return_value = mock_http_result
        patch_form.return_value = mock_form
        mock_form.is_valid.return_value = False

        view = RegistrationView(request=mock_request)
        result = view.post(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_render.assert_called_once_with(mock_request, 'registration/registration.html', {'form': mock_form})
        patch_form.assert_called_once()

    @patch(f'{FILE_PATH}.redirect')
    @patch(f'{FILE_PATH}.RegistrationForm')
    @patch(f'{FILE_PATH}.authenticate')
    @patch(f'{FILE_PATH}.login')
    def test_get_registration_page_valid_form(self, patch_login, patch_authenticate, patch_form, patch_redirect):
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_form = MagicMock()
        mock_user = MagicMock()

        patch_redirect.return_value = mock_http_result
        patch_form.return_value = mock_form
        mock_form.is_valid.return_value = True
        cd = {'username': 'username1', 'password': 'password1', 'email': 'email1@email.ru'}
        mock_form.cleaned_data = cd
        mock_form.save.return_value = mock_user
        patch_authenticate.return_value = mock_user
        patch_login.return_value = mock_user

        view = RegistrationView(request=mock_request)
        result = view.post(mock_request)

        self.assertEqual(result, mock_http_result)
        patch_redirect.assert_called_once_with('account:profile', username='username1')
        patch_form.assert_called_once_with(mock_request.POST)
        mock_form.is_valid.assert_called_once()
        mock_form.save.assert_called_once_with(commit=False)
        mock_user.set_password.assert_called_once_with('password1')
        mock_user.save.assert_called_once()
        patch_authenticate.assert_called_once_with(username='username1', password='password1')
        patch_login.assert_called_once_with(mock_request, mock_user)
