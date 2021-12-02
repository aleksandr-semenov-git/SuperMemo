from django.test import TestCase
from account.forms.profile_forms import PersonalDataEditForm
from memo.forms import AddGoalForm


class PersonalDataEditFormTest(TestCase):
    def setUp(self) -> None:
        self.form = PersonalDataEditForm()

    def test_fields_labels(self):
        self.assertTrue(self.form.fields['username'].label is None)
        self.assertTrue(self.form.fields['email'].label is None)
        self.assertTrue(self.form.fields['first_name'].label is None or
                        self.form.fields['first_name'].label == 'Firstname')
        self.assertTrue(self.form.fields['last_name'].label is None or
                        self.form.fields['last_name'].label == 'Lastname')

    def test_fields_required_false(self):
        self.assertTrue(self.form.fields['username'].required is False)
        self.assertTrue(self.form.fields['email'].required is False)
        self.assertTrue(self.form.fields['first_name'].required is False)
        self.assertTrue(self.form.fields['last_name'].required is False)

    def test_fields_min_length(self):
        self.assertEqual(self.form.fields['username'].min_length, 3)
        self.assertEqual(self.form.fields['first_name'].min_length, 3)
        self.assertEqual(self.form.fields['last_name'].min_length, 3)

    def test_fields_max_length(self):
        self.assertEqual(self.form.fields['username'].max_length, 150)
        self.assertEqual(self.form.fields['first_name'].max_length, 150)
        self.assertEqual(self.form.fields['last_name'].max_length, 150)


class AddGoalFormTest(TestCase):
    def setUp(self) -> None:
        self.form = AddGoalForm()

    def test_fields_labels(self):
        self.assertTrue(self.form.fields['name'].label is None or
                        self.form.fields['name'].label == 'Name your goal')

    def test_fields_labels_min_length(self):
        self.assertEqual(self.form.fields['name'].min_length, 3)

    def test_fields_labels_max_length(self):
        self.assertEqual(self.form.fields['name'].max_length, 150)

    def test_field_name_required_true(self):
        self.assertTrue(self.form.fields['name'].required is True)
