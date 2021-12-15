from unittest.mock import patch, MagicMock
from django.test import TestCase
from account.services.model_service import ProfileService


class ModelServiceTest(TestCase):
    FILE_PATH = 'account.services.model_service'

    @patch(f'{FILE_PATH}.Profile.objects.get_or_create')
    def test_get_or_create_profile(self, patch_profile_get_or_create):
        mock_user = MagicMock()
        mock_profile = MagicMock()
        mock_created = MagicMock()
        patch_profile_get_or_create.return_value = mock_profile, mock_created
        result = ProfileService.get_or_create_profile(mock_user)
        self.assertEqual(result, mock_profile)
        patch_profile_get_or_create.assert_called_once_with(user=mock_user)

    @patch(f'{FILE_PATH}.Profile.objects.create')
    def test_create_profile(self, patch_profile_create):
        mock_user = MagicMock()
        mock_profile = MagicMock()
        patch_profile_create.return_value = mock_profile
        result = ProfileService.create_profile(mock_user)
        self.assertEqual(result, mock_profile)
        patch_profile_create.assert_called_once_with(user=mock_user)

    @patch(f'{FILE_PATH}.Profile.objects.filter')
    def test_profile_exists(self, patch_profile_filter):
        mock_user = MagicMock()
        mock_profile = MagicMock()
        expected_result = True
        patch_profile_filter.return_value = mock_profile
        mock_profile.exists.return_value = expected_result
        result = ProfileService.profile_exists(mock_user)
        self.assertEqual(result, expected_result)
        patch_profile_filter.assert_called_once_with(user=mock_user)
        mock_profile.exists.assert_called_once()
