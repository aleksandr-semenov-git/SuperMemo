from unittest.mock import patch, MagicMock
from django.http import HttpResponse
from django.test import TestCase
from memo.views import HomePage, AddGoalPage


class HomePageTest(TestCase):
    @patch('memo.views.home.render')
    def test_home_page(self, patch_render):
        expected_result = HttpResponse()
        mock_request = MagicMock()
        mock_render_result = MagicMock()
        patch_render.return_value = mock_render_result
        result = HomePage.get(self, mock_request)

        self.assertEqual(result, mock_render_result)
