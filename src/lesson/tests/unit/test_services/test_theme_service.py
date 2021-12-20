from unittest.mock import patch, MagicMock
from django.test import TestCase
from lesson.models import Section, Theme
from lesson.services.model_service import SectionService, ThemeService, LessonService, QuestionService
from django.db.models import Q


class ModelServiceTest(TestCase):
    FILE_PATH = 'lesson.services.model_service'

    @patch(f'{FILE_PATH}.get_object_or_404')
    def test_get_theme_by_id(self, patch_get_404):
        test_id = 1
        mock_404 = MagicMock()
        patch_get_404.return_value = mock_404
        result = ThemeService.get_theme_by_id(test_id)
        self.assertEqual(result, mock_404)
        patch_get_404.assert_called_once_with(Theme, pk=test_id)

    @patch(f'{FILE_PATH}.get_object_or_404')
    def test_get_theme_by_name_and_goal_id(self, patch_get_404):
        test_id = 1
        test_name = 'name'
        mock_404 = MagicMock()
        patch_get_404.return_value = mock_404
        result = ThemeService.get_theme_by_name_and_section_id(test_name, test_id)
        self.assertEqual(result, mock_404)
        patch_get_404.assert_called_once_with(Theme, Q(name=test_name), Q(section__id=test_id))

    @patch(f'{FILE_PATH}.Theme.objects.create')
    def test_create_theme(self, patch_theme_create):
        test_name = 'name'
        mock_theme = MagicMock()
        mock_section = MagicMock()
        patch_theme_create.return_value = mock_theme
        result = ThemeService.create_theme(test_name, mock_section)
        self.assertEqual(result, mock_theme)
        patch_theme_create.assert_called_once_with(name=test_name, section=mock_section)
