from unittest.mock import patch, MagicMock
from django.test import TestCase
from memo.views import GoalPage, AddGoalPage


class GoalPageTest(TestCase):
    @patch('memo.views.goal.render')
    @patch('memo.views.goal.GoalService.get_goal_by_id')
    def test_get_goal_page(self, patch_get_goal_by_id, patch_render):
        mock_request = MagicMock()
        mock_render_result = MagicMock()
        mock_goal = MagicMock()

        patch_get_goal_by_id.return_value = mock_goal
        patch_render.return_value = mock_render_result

        result = GoalPage.get(self, mock_request, 1)
        self.assertEqual(result, mock_render_result)
        patch_render.assert_called_once_with(mock_request, 'goal_page.html', {'goal': mock_goal})

    @patch('memo.views.goal.render')
    @patch('memo.views.goal.AddGoalForm')
    def test_get_addgoal_page(self, patch_form, patch_render):
        mock_request = MagicMock()
        mock_render_result = MagicMock()
        mock_form = MagicMock()

        patch_form.return_value = mock_form
        patch_render.return_value = mock_render_result

        result = AddGoalPage.get(self, mock_request)
        self.assertEqual(result, mock_render_result)
        patch_render.assert_called_once_with(mock_request, 'add_goal.html', {'form': mock_form})

    @patch('memo.views.goal.redirect')
    @patch('memo.views.goal.AddGoalForm')
    @patch('memo.views.goal.GoalService.create_goal')
    def test_post_addgoal_page_valid_form(self, patch_create_goal, patch_form, patch_redirect):
        mock_request = MagicMock()
        mock_request.user = MagicMock()
        mock_profile = MagicMock()
        mock_request.user.profile = mock_profile
        mock_redirect_result = MagicMock()
        cd = {'name': 'testname'}
        mock_form = MagicMock()
        mock_form().cleaned_data = cd
        patch_form.return_value = mock_form
        patch_form().is_valid.return_value = True
        patch_form().cleaned_data = cd

        patch_redirect.return_value = mock_redirect_result

        result = AddGoalPage.post(self, mock_request)
        self.assertEqual(result, mock_redirect_result)
        patch_form.assert_called_with(mock_request.POST)
        patch_create_goal.assert_called_once_with('testname', mock_profile)
        patch_redirect.assert_called_once_with('memo:my_goals')

        call_count = patch_form.call_count
        call_list = patch_form.method_calls
        args_call_list = patch_form.call_args_list

    @patch('memo.views.goal.redirect')
    @patch('memo.views.goal.AddGoalForm')
    def test_post_addgoal_page_invalid_form(self, patch_form, patch_redirect):
        mock_request = MagicMock()
        mock_redirect_result = MagicMock()
        mock_form = MagicMock()
        patch_form.return_value = mock_form

        patch_redirect.return_value = mock_redirect_result
        patch_form().is_valid.return_value = False

        result = AddGoalPage.post(self, mock_request)
        self.assertEqual(result, mock_redirect_result)
        patch_redirect.assert_called_once_with('memo:my_goals')
