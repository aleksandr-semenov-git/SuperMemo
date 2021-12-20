from unittest.mock import patch, MagicMock
from django.test import TestCase
from memo.models import Goal
from memo.services.model_service import GoalService


class ModelServiceTest(TestCase):
    def test_get_goal_by_profile(self):
        mock_profile = MagicMock()
        mock_goals = MagicMock()
        mock_profile.goals.all.return_value = mock_goals
        result = GoalService.get_goals_by_profile(mock_profile)
        self.assertEqual(result, mock_goals)

    @patch('memo.services.model_service.get_object_or_404')
    def test_get_goal_by_id(self, patch_get_404):
        test_goal_id = 1
        mock_404 = MagicMock()
        patch_get_404.return_value = mock_404
        result = GoalService.get_goal_by_id(test_goal_id)
        self.assertEqual(result, mock_404)
        patch_get_404.assert_called_once_with(Goal, pk=1)

    @patch('memo.services.model_service.get_object_or_404')
    def test_get_goal_by_name(self, patch_get_404):
        test_goal_name = 'testname'
        mock_404 = MagicMock()
        patch_get_404.return_value = mock_404
        result = GoalService.get_goal_by_name(test_goal_name)
        self.assertEqual(result, mock_404)
        patch_get_404.assert_called_once_with(Goal, name=test_goal_name)

    @patch('memo.services.model_service.Goal.objects.create')
    def test_create_goal(self, patch_goal_create):
        test_name = 'testname'
        mock_profile = MagicMock()
        mock_goal = MagicMock()
        patch_goal_create.return_value = mock_goal
        result = GoalService.create_goal(test_name, mock_profile)
        self.assertEqual(result, mock_goal)
        patch_goal_create.assert_called_once_with(name=test_name, profile=mock_profile)
