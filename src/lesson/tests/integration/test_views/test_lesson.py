from django.test import TestCase
from lesson.forms import AddEditQuestionForm
from lesson.models import Lesson, Question, Section, Theme
from django.urls import reverse
from datetime import datetime
from memo.models import Goal


class LessonPagesTest(TestCase):
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
        # If transform is provided, values is compared to a list produced by applying transform to each member of qs
        # By default, the comparison is also ordering dependent. If qs doesn’t provide an implicit ordering,
        #   you can set the ordered parameter to False

    def test_get_sure_page(self):
        test_theme_id = 6
        session = self.client.session
        session['goal_id'] = 7
        session.save()
        theme = Theme.objects.get(pk=6)
        section = Section.objects.get(pk=4)
        goal = Goal.objects.get(pk=7)

        login = self.client.login(username='test_user0', password='121212ab')
        result = self.client.get(reverse('lesson:sure', kwargs={'theme_id': test_theme_id}), data={})
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'sure_page.html')
        self.assertEqual(result.context['theme'].id, theme.id)
        self.assertEqual(result.context['theme'], theme)
        self.assertEqual(result.context['section'], section)
        self.assertEqual(result.context['goal'], goal)

    def test_post_sure_page_success(self):
        login = self.client.login(username='test_user0', password='121212ab')
        result = self.client.post(reverse('lesson:sure', kwargs={'theme_id': 6}), data={})
        self.assertRedirects(result, reverse('lesson:lesson_page'), fetch_redirect_response=False)

    def test_get_lesson_page_lesson_id_in_session(self):
        session = self.client.session
        session['active_lesson_id'] = 4
        session.save()
        lesson = Lesson.objects.get(pk=4)

        login = self.client.login(username='test_user0', password='121212ab')
        result = self.client.get(reverse('lesson:lesson_page', kwargs={}), data={})

        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'lesson_learn.html')
        self.assertEqual(result.context['lesson'], lesson)
        self.assertTrue(isinstance(result.context['form'], AddEditQuestionForm))

    def test_get_lesson_page_lesson_id_not_in_session(self):
        expected_lesson_name = f'test_goal_01 test_section_011 {datetime.now().strftime("%Y-%m-%d")}'
        expected_active_lesson_id = 5
        session = self.client.session
        session['goal_id'] = 7
        session['theme_id'] = 6
        session.save()
        goal = Goal.objects.get(pk=7)
        lesson = Lesson.objects.get(pk=4)

        login = self.client.login(username='test_user0', password='121212ab')
        result = self.client.get(reverse('lesson:lesson_page', kwargs={}), data={})
        actual_lesson_name = result.context['lesson'].name

        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'lesson_learn.html')
        self.assertTrue(isinstance(result.context['lesson'], Lesson))
        self.assertEqual(actual_lesson_name, expected_lesson_name)
        self.assertTrue(isinstance(result.context['form'], AddEditQuestionForm))
        self.assertEqual(expected_active_lesson_id, result.context['lesson'].id)
        self.assertNotEqual(lesson.id, result.context['lesson'].id)

    def test_post_lesson_page_valid_form(self):
        session = self.client.session
        session['active_lesson_id'] = 4
        session['theme_id'] = 6
        session.save()

        theme = Theme.objects.get(pk=6)
        lesson = Lesson.objects.get(pk=4)

        login = self.client.login(username='test_user0', password='121212ab')
        result = self.client.post(reverse('lesson:lesson_page', kwargs={}),
                                  data={'question': 'test_q_0111_2', 'answer': 'test_a_0111_2'})

        self.assertRedirects(result, reverse('lesson:lesson_page'), fetch_redirect_response=False)
        expected_question = Question.objects.get(question='test_q_0111_2')
        self.assertEqual(expected_question.theme, theme)
        self.assertEqual(expected_question.lesson, lesson)

    def test_post_lesson_page_not_valid_form(self):
        session = self.client.session
        session['active_lesson_id'] = 4
        session['theme_id'] = 6
        session.save()
        lesson = Lesson.objects.get(pk=4)

        login = self.client.login(username='test_user0', password='121212ab')
        result = self.client.post(reverse('lesson:lesson_page', kwargs={}),
                                  data={'question': '', 'answer': ''})

        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'lesson_learn.html')

        self.assertTrue(isinstance(result.context['form'], AddEditQuestionForm))
        self.assertEqual(result.context['lesson'], lesson)

    def test_get_end_lesson_page(self):
        session = self.client.session
        session['active_lesson_id'] = 4
        session.save()
        lesson = Lesson.objects.get(pk=4)

        login = self.client.login(username='test_user0', password='121212ab')
        result = self.client.get(reverse('lesson:end_lesson', kwargs={}), data={})

        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'end_lesson.html')
        self.assertEqual(result.context['lesson'], lesson)

    def test_post_end_lesson_page_finish_lesson(self):
        session = self.client.session
        session['goal_id'] = 7
        session['theme_id'] = 6
        session['active_lesson_id'] = 4
        session.save()
        goal = Goal.objects.get(pk=7)

        login = self.client.login(username='test_user0', password='121212ab')
        result = self.client.post(reverse('lesson:end_lesson', kwargs={}), data={'end': 'End lesson'})

        self.assertRedirects(result, reverse('memo:goal_page', kwargs={'goal_id': goal.id}))
        self.assertNotIn('active_lesson_id', self.client.session)
        self.assertNotIn('theme_id', self.client.session)

    def test_post_end_lesson_page_not_finish_lesson(self):
        login = self.client.login(username='test_user0', password='121212ab')
        result = self.client.post(reverse('lesson:end_lesson', kwargs={}), data={'end': 'Not End lesson'})
        self.assertRedirects(result, reverse('lesson:lesson_page', kwargs={}), fetch_redirect_response=False)
