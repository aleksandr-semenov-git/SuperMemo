from unittest.mock import patch, MagicMock
from django.test import TestCase
from lesson.services.lesson_service import LessonService


class ModelServiceTest(TestCase):
    FILE_PATH = 'lesson.services.model_service'

    @patch(f'{FILE_PATH}.Lesson.objects.get')
    def test_get_lesson_by_goal_id(self, patch_lesson_get):
        test_id = 1
        mock_lesson = MagicMock()
        patch_lesson_get.return_value = mock_lesson
        result = LessonService.get_lesson_by_id(test_id)
        self.assertEqual(result, mock_lesson)
        patch_lesson_get.assert_called_once_with(pk=test_id)

    @patch(f'{FILE_PATH}.Lesson.objects.filter')
    def test_get_lesson_by_profile(self, patch_lesson_filter):
        mock_lesson = MagicMock()
        mock_profile = MagicMock()
        patch_lesson_filter.return_value = mock_lesson
        result = LessonService.get_lessons_by_profile(mock_profile)
        self.assertEqual(result, mock_lesson)
        patch_lesson_filter.assert_called_once_with(goal__profile=mock_profile)

    @patch(f'{FILE_PATH}.Lesson.objects.create')
    def test_create_lesson(self, patch_lesson_create):
        test_name = 'name'
        mock_goal = MagicMock()
        mock_lesson = MagicMock()
        patch_lesson_create.return_value = mock_lesson
        result = LessonService.create_lesson(test_name, mock_goal)
        self.assertEqual(result, mock_lesson)
        patch_lesson_create.assert_called_once_with(name=test_name, goal=mock_goal)
