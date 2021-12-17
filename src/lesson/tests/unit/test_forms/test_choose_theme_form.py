from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from lesson.forms import ChooseThemeForm


class ThemeFormsTest(SimpleTestCase):
    FILE_PATH = 'lesson.forms'

    @patch(f'{FILE_PATH}.Theme.objects')
    def test_init_section_id_exists(self, patch_theme):
        mock_theme = MagicMock()
        mock_theme.all.return_value = mock_theme
        patch_theme.filter.return_value = mock_theme

        form = ChooseThemeForm(section_id=1)
        self.assertEqual(form.fields['name'].queryset, mock_theme)
        patch_theme.filter.assert_called_once()
