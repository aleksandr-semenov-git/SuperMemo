from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from lesson.forms import ChooseSectionForm


class SectionsFormTest(SimpleTestCase):
    FILE_PATH = 'lesson.forms'

    @patch(f'{FILE_PATH}.Section.objects')
    def test_init_goal_id_exists(self, patch_section):
        mock_section = MagicMock()
        # patch_section.none.return_value = mock_section  # Todo ?
        mock_section.all.return_value = mock_section
        patch_section.filter.return_value = mock_section

        form = ChooseSectionForm(goal_id=1)
        self.assertEqual(form.fields['name'].queryset, mock_section)
        patch_section.filter.assert_called_once()
        # patch_section.none.assert_called_once()  # Todo ?
