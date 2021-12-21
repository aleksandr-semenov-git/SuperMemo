import os
from unittest.mock import patch, MagicMock
from django.http import HttpResponse, HttpResponseRedirect
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

import memo
from memo.forms import AddGoalForm
from memo.tests.factories import UserFactory, ProfileFactory, GoalFactory, SectionFactory, ThemeFactory, LessonFactory,\
    QuestionFactory
from memo.models import Goal
from account.models import Profile
from lesson.models import Section, Theme, Lesson, Question

from django.contrib.auth.models import User


class GoalPagesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.user.set_password('121212test')
        self.user.save()
        self.profile = ProfileFactory(user=self.user)
        self.goal = GoalFactory(profile=self.profile)
        self.goal2 = GoalFactory(profile=self.profile)

    def test_user_get_goal_page(self):
        login = self.client.login(username='test_user0', password='121212test')
        goal = self.goal
        result = self.client.get(reverse('memo:goal_page', kwargs={'goal_id': 1}), data={})
        self.assertTemplateUsed(result, 'goal_page.html')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.context['goal'], goal)

    def test_user_get_goal_page_404(self):
        login = self.client.login(username='test_user0', password='121212test')
        non_exist_goal_id = 199
        result = self.client.get(reverse('memo:goal_page', kwargs={'goal_id': non_exist_goal_id}), data={})
        self.assertEqual(result.status_code, 404)

    def test_user_get_addgoal_page(self):
        login = self.client.login(username='test_user0', password='121212test')
        result = self.client.get(reverse('memo:add_goal'), data={})
        self.assertTemplateUsed(result, 'add_goal.html')
        self.assertEqual(result.status_code, 200)
        self.assertTrue(isinstance(result.context['form'], AddGoalForm))

    def test_user_post_addgoal_page_valid_form(self):
        login = self.client.login(username='test_user0', password='121212test')
        result = self.client.post(reverse('memo:add_goal'), data={'name': 'test_goal_name'})
        self.assertRedirects(result, reverse('memo:my_goals'))
        self.assertTrue(Goal.objects.get(name='test_goal_name'))

    def test_user_post_addgoal_page_not_valid_form(self):
        fail_goal_name = 'xx'
        login = self.client.login(username='test_user0', password='121212test')
        result = self.client.post(reverse('memo:add_goal'), data={'name': fail_goal_name})
        self.assertRedirects(result, reverse('memo:my_goals'))
        with self.assertRaises(memo.models.Goal.DoesNotExist):
            Goal.objects.get(name=fail_goal_name)

    def test_user_get_mygoals_page(self):
        login = self.client.login(username='test_user0', password='121212test')
        result = self.client.get(reverse('memo:my_goals'), data={})
        goals = Goal.objects.all()
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'my_goals.html')
        self.assertEqual(list(result.context['goals']), list(goals))
