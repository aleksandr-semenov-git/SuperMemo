from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from account.forms import LoginForm, RegistrationForm
from django import forms


class LoginFormTest(SimpleTestCase):
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


class RegistrationFormTest(SimpleTestCase):
    FILE_PATH = 'account.forms.login_register_forms'

    def test_clean_email_domain_in_net(self):
        cd = {'username': 'user1', 'password': 'password11',
              'confirm_password': 'password11', 'email': 'user1@example.net'}
        form = RegistrationForm()
        form.cleaned_data = cd
        with self.assertRaisesMessage(forms.ValidationError, 'Registration for domain "net" is impossible'):
            form.clean_email()

    @patch(f'{FILE_PATH}.User.objects.filter')
    def test_clean_email_exists(self, patch_user_filter):
        cd = {'username': 'user1', 'password': 'password11',
              'confirm_password': 'password11', 'email': 'user1@example.com'}
        mock_user = MagicMock()
        patch_user_filter.return_value = mock_user
        mock_user.exists.return_value = True
        form = RegistrationForm()
        form.cleaned_data = cd
        with self.assertRaisesMessage(forms.ValidationError, 'Current email is already registered'):
            form.clean_email()
        patch_user_filter.assert_called_once_with(email='user1@example.com')
        mock_user.exists.assert_called_once()

    @patch(f'{FILE_PATH}.User.objects.filter')
    def test_clean_email_not_exists(self, patch_user_filter):
        cd = {'username': 'user1', 'password': 'password11',
              'confirm_password': 'password11', 'email': 'user1@example.com'}
        mock_user = MagicMock()
        patch_user_filter.return_value = mock_user
        mock_user.exists.return_value = False
        form = RegistrationForm()
        form.cleaned_data = cd

        result = form.clean_email()
        self.assertEqual(result, 'user1@example.com')
        patch_user_filter.assert_called_once_with(email='user1@example.com')

    @patch(f'{FILE_PATH}.User.objects.filter')
    def test_clean_username_exists(self, patch_user_filter):
        cd = {'username': 'user1', 'password': 'password11',
              'confirm_password': 'password11', 'email': 'user1@example.com'}
        mock_user = MagicMock()
        patch_user_filter.return_value = mock_user
        mock_user.exists.return_value = True
        form = RegistrationForm()
        form.cleaned_data = cd
        with self.assertRaisesMessage(forms.ValidationError, 'Current username user1 is already registered'):
            form.clean_username()
        mock_user.exists.assert_called_once_with()

    @patch(f'{FILE_PATH}.User.objects.filter')
    def test_clean_username_not_exists(self, patch_user_filter):
        cd = {'username': 'user1', 'password': 'password11',
              'confirm_password': 'password11', 'email': 'user1@example.com'}
        mock_user = MagicMock()
        patch_user_filter.return_value = mock_user
        mock_user.exists.return_value = False
        form = RegistrationForm()
        form.cleaned_data = cd
        result = form.clean_username()
        self.assertEqual(result, 'user1')
        patch_user_filter.assert_called_once_with(username='user1')
        mock_user.exists.assert_called_once_with()

    def test_clean_password1_is_not_password2(self):
        cd = {'username': 'user1', 'password': 'password11',
              'confirm_password': 'password12', 'email': 'user1@example.com'}
        form = RegistrationForm()
        form.cleaned_data = cd
        with self.assertRaisesMessage(forms.ValidationError, 'Passwords not match'):
            form.clean()

    def test_clean_success(self):
        cd = {'username': 'user1', 'password': 'password11',
              'confirm_password': 'password11', 'email': 'user1@example.com'}
        form = RegistrationForm()
        form.cleaned_data = cd
        result = form.clean()
        self.assertEqual(result, cd)
