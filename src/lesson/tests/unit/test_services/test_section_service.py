from unittest.mock import patch, MagicMock
from django.test import TestCase
from lesson.models import Section
from lesson.services.lesson_service import ThemeService, LessonService, QuestionService
from lesson.services import SectionService
from django.db.models import Q


class ModelServiceTest(TestCase):
    FILE_PATH = 'lesson.services.model_service'

    @patch(f'{FILE_PATH}.get_object_or_404')
    def test_get_section_by_id(self, patch_get_404):
        test_id = 1
        mock_404 = MagicMock()
        patch_get_404.return_value = mock_404
        result = SectionService.get_section_by_id(test_id)
        self.assertEqual(result, mock_404)
        patch_get_404.assert_called_once_with(Section, pk=test_id)

    @patch(f'{FILE_PATH}.get_object_or_404')
    def test_get_section_by_name_and_goal_id(self, patch_get_404):
        test_id = 1
        test_name = 'name'
        mock_404 = MagicMock()
        patch_get_404.return_value = mock_404
        result = SectionService.get_section_by_name_and_goal_id(test_name, test_id)
        self.assertEqual(result, mock_404)
        patch_get_404.assert_called_once_with(Section, Q(name=test_name), Q(goal__id=test_id))

    @patch(f'{FILE_PATH}.Section.objects.create')
    def test_create_section(self, patch_section_create):
        test_name = 'name'
        mock_goal = MagicMock()
        mock_section = MagicMock()
        patch_section_create.return_value = mock_section
        result = SectionService.create_section(test_name, mock_goal)
        self.assertEqual(result, mock_section)
        patch_section_create.assert_called_once_with(name=test_name, goal=mock_goal)
