from unittest.mock import patch, MagicMock
from django.test import TestCase
from memo.views import HomePage


class HomePageTest(TestCase):
    @patch('memo.views.home.render')
    def test_get_home_page(self, patch_render):
        mock_request = MagicMock()
        mock_render_result = MagicMock()

        patch_render.return_value = mock_render_result

        view = HomePage(request=mock_request)
        result = view.get(mock_request)

        self.assertEqual(result, mock_render_result)
        patch_render.assert_called_once_with(mock_request, 'home.html', {})
