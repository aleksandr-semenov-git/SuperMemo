from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from lesson.forms import ChooseThemeForm


class ThemeFormsTest(SimpleTestCase):
    FILE_PATH = 'lesson.forms'

    @patch(f'{FILE_PATH}.Theme.objects')
    @patch(f'{FILE_PATH}.forms.Form.__init__')
    def test_init_goal_id_exists(self, patch_init, patch_theme):
        test_section_id = 1
        mock_theme = MagicMock()
        mock_theme.all.return_value = mock_theme
        patch_theme.filter.return_value = mock_theme
        args = ()
        kwargs = {'section_id': test_section_id}

        ChooseThemeForm.fields = {'name': MagicMock()}
        form = ChooseThemeForm(*args, **kwargs)

        patch_init.assert_called_once_with(*args, **{})

        self.assertEqual(form.fields['name'].queryset, mock_theme)
        patch_theme.filter.assert_called_once_with(section__id=test_section_id)
