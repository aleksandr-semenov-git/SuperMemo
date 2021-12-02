import os
from unittest.mock import patch, MagicMock
from django.http import HttpResponse, HttpResponseRedirect
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from memo.models import Profile, Goal
from memo.views import HomePage, AddGoalPage
from account.views import ProfilePage

os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'


class ProfilePageTest(TestCase):
    def setUp(self):
        number_of_goals = 2
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create(username='testuser',
                                        email='testemail@test.test',
                                        )
        self.user.set_password('121212test')
        self.user.save()
        self.profile = Profile.objects.create(user=self.user)
        for goal_num in range(number_of_goals):
            Goal.objects.create(name=f'TEST_GOAL {goal_num}', profile=self.profile)

    def test_response_from_home_page_view_v1(self):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        resp = HomePage.as_view()(request)
        self.assertEqual(resp.status_code, 200)

    def test_response_from_home_page_view_v2(self):
        resp = self.client.get(reverse('memo:home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'home.html', 'base.html')

    @patch('memo.views.profile.redirect')
    def test_anonymous_get_profile_basic(self, mock_redirect):
        expected_result = HttpResponse()
        mock_redirect.return_value = expected_result
        actual_result = self.client.get(reverse('memo:profile_basic'))
        mock_redirect.assert_called_with('account:login')
        self.assertEqual(actual_result, expected_result)

    @patch('memo.views.profile.redirect')
    def test_user_get_profile_basic(self, mock_redirect):
        expected_result = HttpResponseRedirect(redirect_to='/profile/testuser')
        mock_redirect.return_value = expected_result
        login = self.client.login(username='testuser', password='121212test')
        actual_result = self.client.get(reverse('memo:profile_basic'))
        mock_redirect.assert_called_with('memo:profile', username='testuser')
        self.assertEqual(actual_result, expected_result)

    def test_user_get_profile(self):
        expected_result = HttpResponse()
        login = self.client.login(username='testuser', password='121212test')
        actual_result = self.client.get(reverse('memo:profile', kwargs={'username': 'testuser'}))
        self.assertTemplateUsed(actual_result, 'profile_page.html', 'base.html')
        self.assertEqual(actual_result.status_code, 200)
        self.assertEqual(actual_result.context['profile'], self.profile)
        self.assertEqual(actual_result.context['username'], 'testuser')

        expected_goals = self.profile.goals.all()
        actual_goals = actual_result.context['goals']
        self.assertEqual(list(expected_goals), list(actual_goals))  # Приведение к list работает!

    @patch('memo.views.profile.render')
    @patch('memo.views.profile.User.objects')
    @patch('memo.views.profile.Profile.objects')
    def test_user_get_profile_not_exists(self, mock_profile, mock_user, mock_render):
        expected_result = HttpResponse()
        login = self.client.login(username='testuser', password='121212test')
        factory = RequestFactory()
        request = factory.get('/profile/testuser')
        profile = MagicMock()
        goals = MagicMock()
        request.user = MagicMock()

        mock_user.filter.return_value = mock_user
        mock_user.exists.return_value = False
        mock_profile.create.return_value = profile
        profile.goals.return_value = profile
        profile.goals.all.return_value = goals
        mock_render.return_value = expected_result
        actual_result = ProfilePage.as_view()(request, username='testuser')
        mock_profile.create.assert_called_once_with(id=request.user.id, user=request.user)
        mock_render.assert_called_once_with(request,
                                            'profile_page.html',
                                            {'profile': profile,
                                             'goals': goals,
                                             'username': 'testuser'})

        self.assertEqual(expected_result, actual_result)

    @patch('memo.views.profile.render')
    @patch('memo.views.profile.User.objects')
    def test_user_get_profile_exists(self, mock_user, mock_render):
        expected_result = HttpResponse()
        login = self.client.login(username='testuser', password='121212test')
        factory = RequestFactory()
        request = factory.get('/profile/testuser')
        mock_profile = MagicMock()
        goals = MagicMock()
        request.user = MagicMock()

        mock_user.filter.return_value = mock_user
        mock_user.exists.return_value = True
        request.user.profile = mock_profile
        mock_profile.goals.all.return_value = goals
        mock_render.return_value = expected_result
        actual_result = ProfilePage.as_view()(request, username='testuser')
        mock_render.assert_called_once_with(request,
                                            'profile_page.html',
                                            {'profile': mock_profile,
                                             'goals': goals,
                                             'username': 'testuser'})
        self.assertEqual(expected_result, actual_result)

    @patch('memo.views.profile.render')
    @patch('memo.views.profile.PersonalDataEditForm')
    def test_user_get_edit_page(self, mock_form, mock_render):
        expected_result = HttpResponse()
        form = MagicMock()
        mock_form.return_value = form
        mock_render.return_value = expected_result
        login = self.client.login(username='testuser', password='121212test')
        actual_result = self.client.get(reverse('memo:edit'), data={})
        mock_render.assert_called_once_with(actual_result.wsgi_request, 'edit.html', {'form': form})
        self.assertEqual(expected_result, actual_result)

    @patch('memo.views.profile.redirect')
    @patch('memo.views.profile.PersonalDataEditForm')
    def test_user_post_edit_page_valid_form(self, mock_form, mock_redirect):
        expected_result = HttpResponseRedirect('/profile/testuser')
        mock_form().is_valid.return_value = True
        mock_form().cleaned_data = {'username': 'testuser',
                                    'email': 'testemail@test.test',
                                    'first_name': '',
                                    'last_name': ''}
        mock_redirect.return_value = expected_result
        login = self.client.login(username='testuser', password='121212test')
        actual_result = self.client.post(reverse('memo:edit'), data={})
        mock_redirect.assert_called_once_with('memo:profile', username='testuser')
        self.assertEqual(actual_result, expected_result)

    @patch('memo.views.profile.render')
    @patch('memo.views.profile.PersonalDataEditForm')
    def test_user_post_edit_page_not_valid_form(self, mock_form, mock_render):
        expected_result = HttpResponse()
        form = MagicMock()
        mock_form.return_value = form
        mock_form().is_valid.return_value = False
        mock_render.return_value = expected_result
        login = self.client.login(username='testuser', password='121212test')
        actual_result = self.client.post(reverse('memo:edit'), data={})
        mock_render.assert_called_once_with(actual_result.wsgi_request, 'edit.html', {'form': form})
        self.assertEqual(actual_result, expected_result)

    @patch('memo.views.goal.render')
    @patch('memo.views.goal.Goal.objects')
    def test_user_get_goal(self, mock_goal, mock_render):
        expected_result = HttpResponse()
        login = self.client.login(username='testuser', password='121212test')
        goal = MagicMock()
        mock_goal.get.return_value = goal
        mock_render.return_value = expected_result
        actual_result = self.client.get(reverse('memo:goal_page', kwargs={'goal_id': 1}), data={})
        mock_render.assert_called_once_with(actual_result.wsgi_request, 'goal_page.html', {'goal': goal})
        self.assertEqual(expected_result, actual_result)


    @patch('memo.views.goal.render')
    @patch('memo.views.goal.AddGoalForm')
    def test_user_get_addgoal(self, mock_form, mock_render):
        expected_result = HttpResponse()
        login = self.client.login(username='testuser', password='121212test')
        form = MagicMock()
        mock_form.return_value = form
        mock_render.return_value = expected_result
        actual_result = self.client.get(reverse('memo:add_goal'), data={})
        mock_render.assert_called_once_with(actual_result.wsgi_request, 'add_goal.html', {'form': form})
        self.assertEqual(expected_result, actual_result)

    @patch('memo.views.goal.redirect')
    @patch('memo.views.goal.AddGoalForm')
    @patch('memo.views.goal.Goal.objects.create')
    def test_user_post_addgoal_valid_form(self, mock_create, mock_form, mock_redirect):
        expected_result = HttpResponseRedirect(redirect_to='profile/')
        factory = RequestFactory()
        request = factory.post('/profile/add-goal')
        mock_profile = MagicMock()
        mock_goal = MagicMock()
        request.user = MagicMock()
        request.user.profile = mock_profile
        mock_form().is_valid.return_value = True
        cd = {'name': 'foo'}
        mock_form().cleaned_data = cd
        mock_create.return_value = mock_goal
        mock_redirect.return_value = expected_result

        actual_result = AddGoalPage.as_view()(request)
        mock_create.assert_called_once_with(name='foo', profile=mock_profile)
        mock_redirect.assert_called_once_with('memo:profile_basic')
        self.assertEqual(expected_result, actual_result)

    @patch('memo.views.goal.redirect')
    @patch('memo.views.goal.AddGoalForm')
    def test_user_post_addgoal_invalid_form(self, mock_form, mock_redirect):
        expected_result = HttpResponseRedirect(redirect_to='profile/')
        login = self.client.login(username='testuser', password='121212test')
        mock_form().is_valid.return_value = False
        mock_redirect.return_value = expected_result
        actual_result = self.client.post(reverse('memo:add_goal'))

        mock_redirect.assert_called_once_with('memo:profile_basic')
        self.assertEqual(expected_result, actual_result)
