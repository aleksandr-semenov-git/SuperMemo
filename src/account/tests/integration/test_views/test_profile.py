from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User
from account.forms import PersonalDataEditForm
from memo.forms import AddGoalForm
from memo.models import Goal
from memo.tests.factories import UserFactory, ProfileFactory, GoalFactory


class ProfilePagesTest(TestCase):
    FILE_PATH = 'account.views.login_register'

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.user.set_password('121212test')
        self.user.save()
        self.profile = ProfileFactory(user=self.user)
        self.goal = GoalFactory(profile=self.profile)
        self.goal2 = GoalFactory(profile=self.profile)

    def test_user_get_profile_page(self):
        login = self.client.login(username='test_user0', password='121212test')
        profile = self.profile
        username = self.user.username
        with self.assertNumQueries(5):
            result = self.client.get(reverse('account:profile', kwargs={'username': username}), data={})
        expected_goals_query = Goal.objects.filter(profile=profile)
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'profile_page.html')
        actual_goals_query = result.context['goals']
        self.assertEqual(result.context['goals'].count(), 2)
        self.assertEqual(list(actual_goals_query), list(expected_goals_query))
        self.assertQuerysetEqual(actual_goals_query, expected_goals_query, transform=lambda x: x, ordered=False)
        self.assertEqual(result.context['profile'], profile)
        self.assertEqual(result.context['username'], username)

        Goal.objects.create(name='goal3', profile=self.profile)
        with self.assertNumQueries(5):
            result = self.client.get(reverse('account:profile', kwargs={'username': username}), data={})
        self.assertEqual(result.context['goals'].count(), 3)

    def test_user_get_profile_page_basic(self):
        login = self.client.login(username='test_user0', password='121212test')
        with self.assertNumQueries(2):
            result = self.client.get(reverse('account:profile_basic'), data={})
        self.assertRedirects(result, reverse('account:profile', kwargs={'username': 'test_user0'}))

    def test_anonymous_user_get_profile_page_basic(self):
        with self.assertNumQueries(0):
            result = self.client.get(reverse('account:profile_basic'), data={})
        self.assertRedirects(result, reverse('account:login'))

    def test_user_get_edit_page(self):
        login = self.client.login(username='test_user0', password='121212test')
        with self.assertNumQueries(2):
            result = self.client.get(reverse('account:profile_edit'), data={})
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'edit.html')
        self.assertTrue(isinstance(result.context['form'], PersonalDataEditForm))

    def test_user_post_edit_page_valid_form(self):
        login = self.client.login(username='test_user0', password='121212test')
        with self.assertNumQueries(4):
            result = self.client.post(reverse('account:profile_edit'), data={'username': 'test_user',
                                                                             'email': 'test@test.email'}
                                      )
        self.assertRedirects(result, reverse('account:profile', kwargs={'username': 'test_user'}))

    def test_user_post_edit_page_email_empty(self):
        login = self.client.login(username='test_user0', password='121212test')
        with self.assertNumQueries(2):
            result = self.client.post(reverse('account:profile_edit'), data={'username': 'test_user0',
                                                                             'email': ''}
                                      )
        self.assertFormError(result, 'form', None, 'You cant leave username or email field empty')
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'edit.html')
        self.assertTrue(isinstance(result.context['form'], PersonalDataEditForm))

    def test_user_post_edit_page_username_empty(self):
        login = self.client.login(username='test_user0', password='121212test')
        with self.assertNumQueries(2):
            result = self.client.post(reverse('account:profile_edit'), data={'username': '',
                                                                             'email': 'test@test.email'}
                                      )
        self.assertFormError(result, 'form', None, 'You cant leave username or email field empty')
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'edit.html')
        self.assertTrue(isinstance(result.context['form'], PersonalDataEditForm))

    def test_user_post_edit_page_username_exist(self):
        exist_username = 'test_user1'
        exist_user = User.objects.create(username=exist_username, email='test1@test.email')
        login = self.client.login(username='test_user0', password='121212test')
        with self.assertNumQueries(3):
            result = self.client.post(reverse('account:profile_edit'), data={'username': exist_username,
                                                                             'email': 'test@test.email'}
                                      )
        self.assertFormError(result, 'form', None, 'Login test_user1 already exists')
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'edit.html')
        self.assertTrue(isinstance(result.context['form'], PersonalDataEditForm))

    def test_user_post_edit_page_email_exist(self):
        exist_email = 'test1@test.email'
        exist_user = User.objects.create(username='test_user', email=exist_email)
        login = self.client.login(username='test_user0', password='121212test')
        with self.assertNumQueries(4):
            result = self.client.post(reverse('account:profile_edit'), data={'username': 'test_user1',
                                                                             'email': exist_email}
                                      )
        self.assertFormError(result, 'form', None, 'User with email test1@test.email already exists')
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'edit.html')
        self.assertTrue(isinstance(result.context['form'], PersonalDataEditForm))

    def test_user_post_edit_page_username_and_email_exist(self):
        exist_username = 'test_user1'
        exist_email = 'test1@test.email'
        exist_user = User.objects.create(username=exist_username, email=exist_email)
        login = self.client.login(username='test_user0', password='121212test')
        with self.assertNumQueries(4):
            result = self.client.post(reverse('account:profile_edit'), data={'username': exist_username,
                                                                             'email': exist_email}
                                      )
        self.assertFormError(result, 'form', None, 'Login test_user1 and email test1@test.email already exist')
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'edit.html')
        self.assertTrue(isinstance(result.context['form'], PersonalDataEditForm))

    def test_user_get_addgoal_page(self):
        login = self.client.login(username='test_user0', password='121212test')
        with self.assertNumQueries(2):
            result = self.client.get(reverse('account:add_goal'), data={})
        self.assertTemplateUsed(result, 'add_goal.html')
        self.assertEqual(result.status_code, 200)
        self.assertTrue(isinstance(result.context['form'], AddGoalForm))

    def test_user_post_addgoal_page_valid_form(self):
        login = self.client.login(username='test_user0', password='121212test')
        with self.assertNumQueries(4):
            result = self.client.post(reverse('account:add_goal'), data={'name': 'test_goal_name'})
        self.assertRedirects(result, reverse('account:profile_basic'), fetch_redirect_response=False)
        self.assertTrue(Goal.objects.get(name='test_goal_name'))

    def test_user_post_addgoal_page_not_valid_form(self):
        fail_goal_name = 'xx'
        login = self.client.login(username='test_user0', password='121212test')
        with self.assertNumQueries(2):
            result = self.client.post(reverse('account:add_goal'), data={'name': fail_goal_name})
        self.assertRedirects(result, reverse('account:profile_basic'), fetch_redirect_response=False)
        none_goal = Goal.objects.filter(name=fail_goal_name).first()
        self.assertIsNone(none_goal)

