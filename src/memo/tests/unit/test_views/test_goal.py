from unittest.mock import patch, MagicMock
from django.test import TestCase
from memo.views import GoalPage


class GoalPagesTest(TestCase):
    @patch('memo.views.goal.render')
    @patch('memo.views.goal.GoalService.get_goal_by_id')
    def test_get_goal_page(self, patch_get_goal_by_id, patch_render):
        test_goal_id = 1
        mock_request = MagicMock(session={})
        mock_render_result = MagicMock()
        mock_goal = MagicMock()

        patch_get_goal_by_id.return_value = mock_goal
        patch_render.return_value = mock_render_result

        view = GoalPage(request=mock_request)
        result = view.get(mock_request, test_goal_id)

        self.assertEqual(result, mock_render_result)
        self.assertEqual(mock_request.session['goal_id'], test_goal_id)
        patch_get_goal_by_id.assert_called_once_with(test_goal_id)
        patch_render.assert_called_once_with(mock_request, 'goal_page.html', {'goal': mock_goal})
