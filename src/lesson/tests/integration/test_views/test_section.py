from django.test import TestCase
from lesson.forms import LearningForm, ChooseSectionForm, AddSectionForm
from lesson.models import Lesson, Question, Section, Theme
from django.urls import reverse
from memo.models import Goal


class SectionPagesTest(TestCase):
    fixtures = ['all_fixtures.json']

    def test_get_choose_section_page(self):
        session = self.client.session
        session['goal_id'] = 7
        session.save()
        goal = Goal.objects.get(pk=7)

        login = self.client.login(username='test_user0', password='121212ab')
        result = self.client.get(reverse('lesson:choose_section', kwargs={}), data={})

        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'choose_section.html')
        self.assertEqual(result.context['goal'], goal)
        self.assertTrue(isinstance(result.context['form'], ChooseSectionForm))

    def test_post_choose_section_page_invalid_form(self):
        session = self.client.session
        session['goal_id'] = 7
        session.save()
        goal = Goal.objects.get(pk=7)

        login = self.client.login(username='test_user0', password='121212ab')
        result = self.client.post(reverse('lesson:choose_section', kwargs={}), data={})

        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'choose_section.html')
        self.assertEqual(result.context['goal'], goal)
        self.assertTrue(isinstance(result.context['form'], ChooseSectionForm))

    def test_get_add_section_page(self):
        login = self.client.login(username='test_user0', password='121212ab')
        result = self.client.get(reverse('lesson:add_section', kwargs={}), data={})
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'add_section.html')
        self.assertTrue(isinstance(result.context['form'], AddSectionForm))

    def test_post_add_section_valid_form(self):
        session = self.client.session
        session['goal_id'] = 7
        session.save()
        goal = Goal.objects.get(pk=7)

        login = self.client.login(username='test_user0', password='121212ab')
        result = self.client.post(reverse('lesson:add_section', kwargs={}), data={'name': 'Valid_name'})

        self.assertRedirects(result,
                             reverse('memo:goal_page', kwargs={'goal_id': goal.id}),
                             fetch_redirect_response=False)
        self.assertTrue(Section.objects.get(name='Valid_name'))

    def test_post_add_section_invalid_form(self):
        session = self.client.session
        session['goal_id'] = 7
        session.save()
        goal = Goal.objects.get(pk=7)

        login = self.client.login(username='test_user0', password='121212ab')
        result = self.client.post(reverse('lesson:add_section', kwargs={}), data={})

        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'add_section.html')
        self.assertTrue(isinstance(result.context['form'], AddSectionForm))
