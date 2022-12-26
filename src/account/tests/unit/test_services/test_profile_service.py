from unittest.mock import patch, MagicMock
from django.test import TestCase
from account.services.profile_service import ProfileService


class ModelServiceTest(TestCase):
    FILE_PATH = 'account.services.profile_service'

    @patch(f'{FILE_PATH}.Profile.objects.get_or_create')
    def test_get_or_create_profile(self, patch_profile_get_or_create):
        mock_user = MagicMock()
        mock_profile = MagicMock()
        mock_created = MagicMock()
        patch_profile_get_or_create.return_value = mock_profile, mock_created
        result = ProfileService.get_or_create_profile(mock_user)
        self.assertEqual(result, mock_profile)
        patch_profile_get_or_create.assert_called_once_with(user=mock_user)
