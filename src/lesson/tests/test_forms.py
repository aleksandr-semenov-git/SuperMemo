from django.test import TestCase
import datetime
from django.utils import timezone

from lesson.forms import LearningForm, ChooseSectionForm, ChooseThemeForm, AddSectionForm, AddThemeForm
from memo.forms import PersonalDataEditForm, AddGoalForm
from django.contrib.auth.models import User

from memo.models import Section, Theme


class LearningFormTest(TestCase):
    def setUp(self) -> None:
        self.form = LearningForm()

    def test_fields_labels(self):
        self.assertTrue(self.form.fields['question'].label is None)
        self.assertTrue(self.form.fields['answer'].label is None)

    def test_fields_required_true(self):
        self.assertTrue(self.form.fields['question'].required is True)
        self.assertTrue(self.form.fields['answer'].required is True)

    def test_fields_max_length(self):
        self.assertEqual(self.form.fields['question'].max_length, 500)
        self.assertEqual(self.form.fields['answer'].max_length, 500)


class ChooseSectionFormTest(TestCase):
    def setUp(self) -> None:
        self.form = ChooseSectionForm()

    def test_fields_queryset_type(self):
        q_set = Section.objects.all()
        self.assertEqual(self.form.fields['name'].queryset.query.base_table, q_set.query.base_table)

    def test_fields_empty_label(self):
        self.assertEqual(self.form.fields['name'].empty_label, 'Choose chapter')


class ChooseThemeFormTest(TestCase):
    def setUp(self) -> None:
        self.form = ChooseThemeForm()

    def test_fields_queryset_type(self):
        q_set = Theme.objects.all()
        self.assertEqual(self.form.fields['name'].queryset.query.base_table, q_set.query.base_table)

    def test_fields_empty_label(self):
        self.assertEqual(self.form.fields['name'].empty_label, 'Choose theme')


class AddSectionFormTest(TestCase):
    def setUp(self) -> None:
        self.form = AddSectionForm()

    def test_fields_labels(self):
        self.assertTrue(self.form.fields['name'].label is None
                        or self.form.fields['name'].label == 'Name your section')

    def test_fields_required_true(self):
        self.assertTrue(self.form.fields['name'].required is True)

    def test_fields_max_length(self):
        self.assertEqual(self.form.fields['name'].max_length, 150)

    def test_fields_min_length(self):
        self.assertEqual(self.form.fields['name'].min_length, 3)


class AddThemeFormTest(TestCase):
    def setUp(self) -> None:
        self.form = AddThemeForm()

    def test_fields_labels(self):
        self.assertTrue(self.form.fields['name'].label is None
                        or self.form.fields['name'].label == 'Name your theme')

    def test_fields_required_true(self):
        self.assertTrue(self.form.fields['name'].required is True)

    def test_fields_max_length(self):
        self.assertEqual(self.form.fields['name'].max_length, 150)

    def test_fields_min_length(self):
        self.assertEqual(self.form.fields['name'].min_length, 3)
