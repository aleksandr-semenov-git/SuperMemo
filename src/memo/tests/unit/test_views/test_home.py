from unittest.mock import patch, MagicMock
from django.http import HttpResponse
from django.test import TestCase
from memo.views import HomePage, AddGoalPage


class HomePageTest(TestCase):
    @patch('memo.views.home.render')
    def test_get_home_page(self, patch_render):
        mock_request = MagicMock()
        mock_render_result = MagicMock()
        patch_render.return_value = mock_render_result
        result = HomePage.get(self, mock_request)

        self.assertEqual(result, mock_render_result)
        patch_render.assert_called_once_with(mock_request, 'home.html', {})
