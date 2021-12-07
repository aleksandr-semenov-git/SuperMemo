import os
from unittest.mock import patch, MagicMock
from django.http import HttpResponse, HttpResponseRedirect
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from memo.models import Profile, Goal
from memo.views import HomePage, AddGoalPage
from account.views import ProfilePage
from memo.services.model_service import ProfileService, GoalService
from lesson.services.model_service import SectionService, ThemeService, LessonService

os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'


class ModelServiceTest(TestCase):
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

    # @patch('memo.services.model_service.Profile.objects')
    # def test_get_or_create_profile(self, mock_profile):
    #     expected_result = (Profile(), bool)
    #     mock_profile.get_or_create().return_value = expected_result
    #     actual_result = ProfileService.get_or_create_profile()
    #     self.assertEqual(actual_result, expected_result)

    def test1(self):
        self.assertEqual(1, 1)

