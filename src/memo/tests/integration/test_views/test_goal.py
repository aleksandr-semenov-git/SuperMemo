from memo.forms import AddGoalForm
from memo.tests.factories import UserFactory, ProfileFactory, GoalFactory
from memo.models import Goal
from django.urls import reverse
from django.test import TestCase, RequestFactory, Client


class GoalPagesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.user.set_password('121212test')
        self.user.save()
        self.profile = ProfileFactory(user=self.user)
        self.goal1 = GoalFactory(profile=self.profile)
        self.goal2 = GoalFactory(profile=self.profile)

    def test_user_get_goal_page(self):
        login = self.client.login(username='test_user0', password='121212test')
        goal = self.goal1
        with self.assertNumQueries(7):
            result = self.client.get(reverse('memo:goal_page', kwargs={'goal_id': 1}), data={})
        result = self.client.get(reverse('memo:goal_page', kwargs={'goal_id': 1}), data={})
        self.assertTemplateUsed(result, 'goal_page.html')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.context['goal'], goal)

    def test_user_get_goal_page_404(self):
        login = self.client.login(username='test_user0', password='121212test')
        non_exist_goal_id = 199
        with self.assertNumQueries(3):
            result = self.client.get(reverse('memo:goal_page', kwargs={'goal_id': non_exist_goal_id}), data={})
        self.assertEqual(result.status_code, 404)

    def test_user_get_addgoal_page(self):
        login = self.client.login(username='test_user0', password='121212test')
        with self.assertNumQueries(2):
            result = self.client.get(reverse('memo:add_goal'), data={})
        self.assertTemplateUsed(result, 'add_goal.html')
        self.assertEqual(result.status_code, 200)
        self.assertTrue(isinstance(result.context['form'], AddGoalForm))

    def test_user_post_addgoal_page_valid_form(self):
        login = self.client.login(username='test_user0', password='121212test')
        with self.assertNumQueries(4):
            result = self.client.post(reverse('memo:add_goal'), data={'name': 'test_goal_name'})
        self.assertRedirects(result, reverse('memo:my_goals'))
        self.assertTrue(Goal.objects.get(name='test_goal_name'))

    def test_user_post_addgoal_page_not_valid_form(self):
        fail_goal_name = 'xx'
        login = self.client.login(username='test_user0', password='121212test')
        with self.assertNumQueries(2):
            result = self.client.post(reverse('memo:add_goal'), data={'name': fail_goal_name})
        self.assertRedirects(result, reverse('memo:my_goals'))
        none_goal = Goal.objects.filter(name=fail_goal_name).first()
        self.assertIsNone(none_goal)

    def test_user_get_mygoals_page(self):
        login = self.client.login(username='test_user0', password='121212test')
        with self.assertNumQueries(4):
            result = self.client.get(reverse('memo:my_goals'), data={})
        expected_goals_query = Goal.objects.filter(profile=self.profile)
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'my_goals.html')
        actual_goals_query = result.context['goals']
        self.assertEqual(list(actual_goals_query), list(expected_goals_query))
        self.assertQuerysetEqual(actual_goals_query, expected_goals_query, transform=lambda x: x, ordered=False)
        self.assertEqual(result.context["goals"].count(), 2)

        Goal.objects.create(name='goal3', profile=self.profile)
        with self.assertNumQueries(4):
            result = self.client.get(reverse('memo:my_goals'), data={})
        self.assertEqual(result.context["goals"].count(), 3)
