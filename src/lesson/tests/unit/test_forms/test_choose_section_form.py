from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase
from lesson.forms import ChooseSectionForm


class SectionsFormTest(SimpleTestCase):
    FILE_PATH = 'lesson.forms'

    @patch(f'{FILE_PATH}.Section.objects')
    @patch(f'{FILE_PATH}.forms.Form.__init__')
    def test_init_goal_id_exists(self, patch_init, patch_section):
        goal_id = 1
        mock_section = MagicMock()
        mock_section.all.return_value = mock_section
        patch_section.filter.return_value = mock_section
        args = ()
        kwargs = {'goal_id': goal_id}

        ChooseSectionForm.fields = {'name': MagicMock()}
        form = ChooseSectionForm(*args, **kwargs)

        patch_init.assert_called_once_with(*args, **{})

        self.assertEqual(form.fields['name'].queryset, mock_section)
        patch_section.filter.assert_called_once_with(goal__id=goal_id)
