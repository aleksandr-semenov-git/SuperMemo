from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from memo.tests.factories import UserFactory, ProfileFactory, GoalFactory


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
