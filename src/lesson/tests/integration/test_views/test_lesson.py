from django.test import TestCase
from lesson.models import Lesson, Question, Section, Theme
from django.urls import reverse


class LessonTestCase(TestCase):
    fixtures = ['all_fixtures.json']

    def test_get_mylessons_page(self):
        login = self.client.login(username='test_user0', password='121212ab')

        result = self.client.get(reverse('lesson:my_lessons'), data={})
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'my_lessons.html')

        expected_lessons_query = Lesson.objects.filter(goal__profile__user__username='test_user0')
        actual_lessons_query = result.context['lessons']
        self.assertQuerysetEqual(actual_lessons_query, expected_lessons_query, transform=lambda x: x, ordered=False)

        goal = actual_lessons_query.first().goal
        Lesson.objects.create(goal=goal, name=100)

        result = self.client.get(reverse('lesson:my_lessons'), data={})
        expected_lessons_query = Lesson.objects.filter(goal__profile__user__username='test_user0')
        actual_lessons_query = result.context['lessons']
        self.assertQuerysetEqual(actual_lessons_query, expected_lessons_query, transform=lambda x: x, ordered=False)
        # Что должно произойти, чтобы этот код упал?
        # Не знаю, что должно произойти, но если оно произойдёт, я об этом узнаю
