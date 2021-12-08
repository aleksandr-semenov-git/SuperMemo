import os
from unittest.mock import patch, MagicMock

from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from memo.models import Goal
from account.models import Profile
from memo.views import HomePage, AddGoalPage
from account.views import ProfilePage
from memo.services.model_service import GoalService
from account.services.model_service import ProfileService
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
            Goal.objects.create(name=f'goal{goal_num}', profile=self.profile)


    @patch('memo.services.model_service.get_object_or_404')
    def test_get_goal_by_id(self, mock_get_404):
        goal_id = 1
        expected_result = (Goal(), bool)
        actual_result = GoalService.get_goal_by_id(goal_id)
        mock_get_404.assert_called_once_with(Goal, goal_id)

    # @patch('memo.services.model_service.GoalService.get_goals_by_profile')
    # def test_get_goals_by_profile(self, mock_goal_service):
    #     expected_result = QuerySet()
    #     mock_goal_service.return_value =
    #     profile = MagicMock()
    #     profile.goals.return_value = profile
    #     profile.goals.all.return_value = QuerySet()
    #     actual_result = GoalService.get_goals_by_profile(profile=profile)
    #     self.assertEqual(actual_result, expected_result)


#         expected_result = (Profile(), bool)
#         mock_profile.get_or_create().return_value = expected_result
#         actual_result = GoalService.get_goals_by_profile(profile)