from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from account.forms import LoginForm, RegistrationForm
from django import forms


class AccountFormsTest(SimpleTestCase):
    FILE_PATH = 'account.forms.login_register_forms'

    @patch(f'{FILE_PATH}.User.objects')
    def test_login_form_user_not_exists(self, patch_user_model):
        cd = {'username': 'user1', 'password': 'password11'}
        mock_user = MagicMock()

        patch_user_model.filter.return_value = mock_user
        mock_user.exists.return_value = False

        form = LoginForm()
        form.cleaned_data = cd
        with self.assertRaisesMessage(forms.ValidationError, 'User with login user1 not found.'):
            form.clean_username()
            self.assertEqual(form.clean_username(), 'user1')
        patch_user_model.filter.assert_called_once_with(username='user1')
        mock_user.exists.assert_called_once()

    @patch(f'{FILE_PATH}.User.objects')
    def test_login_form_user_exists_check_password_false(self, patch_user_model):
        cd = {'username': 'user1', 'password': 'password11'}
        mock_user = MagicMock()

        patch_user_model.filter.return_value = mock_user
        mock_user.first.return_value = mock_user
        mock_user.check_password.return_value = False

        form = LoginForm()
        form.cleaned_data = cd

        with self.assertRaisesMessage(forms.ValidationError, 'Incorrect password'):
            form.clean_password()
        patch_user_model.filter.assert_called_once_with(username='user1')
        mock_user.first.assert_called_once()
        mock_user.check_password.assert_called_once_with('password11')

    @patch(f'{FILE_PATH}.User.objects')
    def test_login_form_user_exists_check_password_true(self, patch_user_model):
        cd = {'username': 'user1', 'password': 'password11'}
        mock_user = MagicMock()

        patch_user_model.filter.return_value = mock_user
        mock_user.first.return_value = mock_user
        mock_user.check_password.return_value = True

        form = LoginForm()
        form.cleaned_data = cd
        result = form.clean_password()

        self.assertEqual(result, 'password11')
        patch_user_model.filter.assert_called_once_with(username='user1')
        mock_user.first.assert_called_once()
        mock_user.check_password.assert_called_once_with('password11')

