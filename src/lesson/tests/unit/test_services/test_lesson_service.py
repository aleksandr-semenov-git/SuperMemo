from unittest.mock import patch, MagicMock
from django.test import TestCase
from lesson.services.lesson_service import LessonService


class ModelServiceTest(TestCase):
    FILE_PATH = 'lesson.services.lesson_service'

    @patch(f'{FILE_PATH}.Lesson.objects.get')
    def test_get_lesson_by_id(self, patch_lesson_get):
        test_id = 1
        mock_lesson = MagicMock()
        patch_lesson_get.return_value = mock_lesson
        result = LessonService.get_lesson_by_id(test_id)
        self.assertEqual(result, mock_lesson)
        patch_lesson_get.assert_called_once_with(pk=test_id)

    @patch(f'{FILE_PATH}.Lesson.objects.get')
    def test_get_lesson_by_theme_id(self, patch_lesson_get):
        test_id = 1
        mock_lesson = MagicMock()
        patch_lesson_get.return_value = mock_lesson
        result = LessonService.get_lesson_by_theme_id(test_id)
        self.assertEqual(result, mock_lesson)
        patch_lesson_get.assert_called_once_with(theme__id=test_id)

    @patch(f'{FILE_PATH}.Lesson.objects.filter')
    def test_get_lesson_by_profile(self, patch_lesson_filter):
        mock_lesson = MagicMock()
        mock_profile = MagicMock()
        patch_lesson_filter.return_value = mock_lesson
        result = LessonService.get_lessons_by_profile(mock_profile)
        self.assertEqual(result, mock_lesson)
        patch_lesson_filter.assert_called_once_with(goal__profile=mock_profile)

    @patch(f'{FILE_PATH}.Lesson.objects.get_or_create')
    def test_get_or_create_lesson(self, patch_lesson_create):
        test_goal_name = 'name1'
        test_section_name = 'name2'
        test_theme_name = 'name3'
        mock_lesson = MagicMock()
        mock_goal = MagicMock()
        mock_section = MagicMock()
        mock_theme = MagicMock()

        created = True
        mock_goal.name = test_goal_name
        mock_section.name = test_section_name
        mock_theme.name = test_theme_name
        mock_theme.section = mock_section
        patch_lesson_create.return_value = mock_lesson, created

        result = LessonService.get_or_create_lesson(mock_goal, mock_theme)

        self.assertEqual(result, mock_lesson)
        patch_lesson_create.assert_called_once_with(name='name1 name2 name3', goal=mock_goal, theme=mock_theme)
