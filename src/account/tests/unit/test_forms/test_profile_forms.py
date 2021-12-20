from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from account.forms import PersonalDataEditForm
from django import forms


class AccountFormsTest(SimpleTestCase):
    FILE_PATH = 'account.forms.login_register_forms'

    def test_edit_form_username_empty_list(self):
        cd = {'username': '', 'password': 'password11', 'email': 'user1@example.com'}

        form = PersonalDataEditForm()
        form.cleaned_data = cd
        with self.assertRaisesMessage(forms.ValidationError, 'You cant leave username or email field empty'):
            form.clean()

    def test_edit_form_email_empty_list(self):
        cd = {'username': 'user1', 'password': 'password11', 'email': ''}

        form = PersonalDataEditForm()
        form.cleaned_data = cd
        with self.assertRaisesMessage(forms.ValidationError, 'You cant leave username or email field empty'):
            form.clean()

    def test_edit_form_username_email_empty_list(self):
        cd = {'username': '', 'password': 'password11', 'email': ''}

        form = PersonalDataEditForm()
        form.cleaned_data = cd
        with self.assertRaisesMessage(forms.ValidationError, 'You cant leave username or email field empty'):
            form.clean()

    @patch(f'{FILE_PATH}.User.objects')
    def test_edit_form_username_in_chd_and_exists__email_in_chd_and_exists(self, patch_user_model):
        expected_exists_call_count = 2
        cd = {'username': 'user1', 'password': 'password11', 'email': 'user1@example.com'}
        chd = ['username', 'email']
        mock_user = MagicMock()

        patch_user_model.filter.return_value = mock_user
        mock_user.exists.return_value = True

        form = PersonalDataEditForm()
        form.cleaned_data = cd
        form.changed_data = chd
        with self.assertRaisesMessage(forms.ValidationError, 'Login user1 and email user1@example.com already exist'):
            form.clean()
        call_args_list = patch_user_model.filter.call_args_list
        expected_call_args_list = ['user1', 'user1@example.com']
        for i, call in enumerate(call_args_list):
            call.assert_called_once_with(expected_call_args_list[i])
        actual_exists_call_count = mock_user.exists.call_count
        self.assertEqual(actual_exists_call_count, expected_exists_call_count)

    @patch(f'{FILE_PATH}.User.objects')
    def test_edit_form_username_in_chd_and_exists__email_not_in_chd(self, patch_user_model):
        cd = {'username': 'user1', 'password': 'password11', 'email': 'user1@example.com'}
        chd = ['username']
        mock_user = MagicMock()

        patch_user_model.filter.return_value = mock_user
        mock_user.exists.return_value = True

        form = PersonalDataEditForm()
        form.cleaned_data = cd
        form.changed_data = chd
        with self.assertRaisesMessage(forms.ValidationError, 'Login user1 already exists'):
            form.clean()
        patch_user_model.filter.assert_called_once_with(username='user1')
        mock_user.exists.assert_called_once()

    @patch(f'{FILE_PATH}.User.objects')
    def test_edit_form_email_in_chd_and_user_exists(self, patch_user_model):
        cd = {'username': 'user1', 'password': 'password11', 'email': 'user1@example.com'}
        chd = ['email']
        mock_user = MagicMock()

        patch_user_model.filter.return_value = mock_user
        mock_user.exists.return_value = True

        form = PersonalDataEditForm()
        form.cleaned_data = cd
        form.changed_data = chd
        with self.assertRaisesMessage(forms.ValidationError, 'User with email user1@example.com already exists'):
            form.clean()
        patch_user_model.filter.assert_called_once_with(email='user1@example.com')
        mock_user.exists.assert_called_once()
