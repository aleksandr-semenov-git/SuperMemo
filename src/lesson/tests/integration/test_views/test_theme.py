from django.test import TestCase
from django.urls import reverse

from lesson.forms import AddThemeForm
from lesson.models import Theme
from memo.models import Goal


class ThemePagesTest(TestCase):
    fixtures = ['lesson_fixtures.json']

    def test_get_add_theme_page(self):
        section_id = 5
        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.get(reverse('lesson:add_theme', kwargs={'section_id': section_id}), data={})
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'add_theme.html')
        self.assertTrue(isinstance(result.context['form'], AddThemeForm))

    def test_post_add_theme_valid_form(self):
        section_id = 5
        session = self.client.session
        test_goal_id = 4
        session['goal_id'] = test_goal_id
        session.save()
        goal = Goal.objects.get(pk=test_goal_id)

        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.post(reverse('lesson:add_theme', kwargs={'section_id': section_id}),
                                  data={'name': 'Valid_name'})

        self.assertRedirects(result,
                             reverse('memo:goal_page', kwargs={'goal_id': goal.id}),
                             fetch_redirect_response=False)
        expected_theme = Theme.objects.filter(name='Valid_name').first()
        self.assertTrue(expected_theme)
        self.assertEqual(expected_theme.section.name, 'TEST2S')

    def test_post_add_theme_invalid_form(self):
        section_id = 5
        test_goal_id = 4
        session = self.client.session
        session['goal_id'] = test_goal_id
        session.save()
        goal = Goal.objects.get(pk=test_goal_id)

        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.post(reverse('lesson:add_theme', kwargs={'section_id': section_id}),
                                  data={})

        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'add_theme.html')
        self.assertTrue(isinstance(result.context['form'], AddThemeForm))
