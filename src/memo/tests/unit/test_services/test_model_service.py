import os
from unittest.mock import patch, MagicMock
from django.test import TestCase
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
    @patch('memo.services.model_service.get_object_or_404')
    @patch('memo.services.model_service.Goal')
    def test_get_goal_by_id(self, goal_patch, get_404_patch):
        goal_id = 1
        expected_result = MagicMock()
        get_404_patch.return_value = expected_result

        actual_result = GoalService.get_goal_by_id(goal_id)
        get_404_patch.assert_called_once_with(goal_patch, goal_id)
