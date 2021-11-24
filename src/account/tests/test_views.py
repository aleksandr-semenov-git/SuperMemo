from unittest.mock import patch
from django.http import HttpResponse, HttpResponseRedirect
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from unittest.mock import MagicMock
from memo.models import Profile, Goal
from django.urls import reverse


class AccountTest(TestCase):
    def setUp(self):
        number_of_goals = 2
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create(username='testuser1',
                                        email='testemail@test.test',
                                        )
        self.not_active_user = User.objects.create(username='not_active_user',
                                                   email='testemail@test.test',
                                                   )
        self.user.set_password('121212test')
        self.user.save()
        self.not_active_user.set_password('121212test')
        self.not_active_user.save()
        self.not_active_user.is_active = False
        self.not_active_user.save()
        self.profile = Profile.objects.create(user=self.user)
        for goal_num in range(number_of_goals):
            Goal.objects.create(name=f'TEST_GOAL {goal_num}', profile=self.profile)

    @patch('account.views.redirect')
    @patch('account.views.LoginForm')
    def test_login_view_not_valid_form(self, mock_login_form, mock_redirect):
        expected_result = HttpResponse()
        mock_login_form().is_valid.return_value = False
        mock_redirect.return_value = expected_result
        actual_result = self.client.post(reverse('account:login'), data={})
        mock_redirect.assert_called_with('account:login')
        self.assertEqual(actual_result, expected_result)

    @patch('account.views.authenticate')
    @patch('account.views.LoginForm')
    def test_login_view_post_user_is_none(self, mock_login_form, mock_authenticate):
        expected_result = HttpResponse('Invalid login')
        mock_login_form().is_valid.return_value = True
        mock_authenticate.return_value = None
        actual_result = self.client.post(reverse('account:login'), data={})
        self.assertEqual(actual_result.content, expected_result.content)
        self.assertEqual(actual_result.status_code, 200)

    @patch('account.views.authenticate')
    @patch('account.views.LoginForm')
    def test_login_view_post_inactive_user(self, mock_login_form, mock_authenticate):
        expected_result = HttpResponse('Disabled account')
        mock_login_form().is_valid.return_value = True
        mock_authenticate.return_value = self.not_active_user
        actual_result = self.client.post(reverse('account:login'), data={})
        self.assertEqual(actual_result.content, expected_result.content)
        self.assertEqual(actual_result.status_code, 200)

    @patch('account.views.redirect')
    @patch('account.views.authenticate')
    @patch('account.views.LoginForm')
    def test_login_view_valid_form_active_user(self, mock_login_form, mock_authenticate, mock_redirect):
        expected_result = HttpResponse()
        mock_login_form().is_valid.return_value = True
        mock_authenticate.return_value = self.user
        mock_login_form().cleaned_data = {'username': 'testuser1', 'password': '121212test'}
        mock_redirect.return_value = expected_result
        actual_result = self.client.post(reverse('account:login'), data={})
        mock_redirect.assert_called_with('memo:profile', username='testuser1')
        self.assertEqual(actual_result, expected_result)
        self.assertEqual(actual_result.status_code, 200)

    @patch('account.views.redirect')
    def test_logout_view(self, mock_redirect):
        expected_result = HttpResponseRedirect(redirect_to='/')
        mock_redirect.return_value = expected_result
        login = self.client.login(username='testuser1', password='121212test')
        actual_result = self.client.get(reverse('account:logout'), data={})
        mock_redirect.assert_called_with('memo:home')

    @patch('account.views.render')
    @patch('account.views.RegistrationForm')
    def test_user_get_registration_view(self, mock_registration_form, mock_render):
        expected_result = HttpResponse()
        form = MagicMock
        mock_render.return_value = expected_result
        mock_registration_form.return_value = form
        actual_result = self.client.get(reverse('account:registration'), data={})
        mock_render.assert_called_with(actual_result.wsgi_request, 'registration/registration.html', {'form': form})
        self.assertEqual(actual_result, expected_result)
        self.assertEqual(actual_result.status_code, 200)

    @patch('account.views.render')
    @patch('account.views.RegistrationForm')
    def test_user_post_registration_view_not_valid_form(self, mock_registration_form, mock_render):
        expected_result = HttpResponse()
        mock_registration_form().is_valid.return_value = False
        form = MagicMock
        mock_registration_form.return_value = form
        mock_render.return_value = expected_result
        actual_result = self.client.get(reverse('account:registration'), data={})
        mock_render.assert_called_with(actual_result.wsgi_request, 'registration/registration.html', {'form': form})
        self.assertEqual(actual_result, expected_result)
        self.assertEqual(actual_result.status_code, 200)

    @patch('account.views.redirect')
    @patch('account.views.RegistrationForm')
    def test_user_post_registration_view_valid_form(self, mock_registration_form, mock_redirect):
        expected_result = HttpResponseRedirect(redirect_to='/profile/testuser1')
        mock_registration_form().is_valid.return_value = True
        mock_registration_form().cleaned_data = {'username': 'testuser1',
                                                 'password': '121212test',
                                                 'email': 'testemail@test.test'}
        mock_redirect.return_value = expected_result
        actual_result = self.client.post(reverse('account:registration'), data={})
        mock_redirect.assert_called_once_with('memo:profile', username='testuser1')
        self.assertEqual(actual_result, expected_result)
        self.assertEqual(actual_result.status_code, 302)
