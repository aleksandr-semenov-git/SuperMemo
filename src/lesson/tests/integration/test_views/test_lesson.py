from django.test import TestCase
from django.urls import reverse

from lesson.forms import AddEditQuestionForm
from lesson.models import Lesson, Question


class LessonPagesTest(TestCase):
    fixtures = ['all_fixtures.json']

    def test_get_lesson_learn_page(self):
        session = self.client.session
        session['goal_id'] = 4
        session.save()
        lesson = Lesson.objects.get(pk=5)

        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.get(reverse('lesson:lesson_learn', kwargs={'theme_id': 5}), data={})

        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'lesson_learn.html')
        self.assertEqual(result.context['lesson'], lesson)
        self.assertTrue(isinstance(result.context['form'], AddEditQuestionForm))

    def test_post_lesson_learn_page_valid_form(self):
        test_question = 'test_q_11'
        test_answer = 'test_a_11'

        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.post(reverse('lesson:lesson_learn', kwargs={'theme_id': 5}),
                                  data={'question': test_question, 'answer': test_answer})
        self.assertRedirects(result,
                             reverse('lesson:lesson_learn', kwargs={'theme_id': 5}),
                             fetch_redirect_response=False)

    def test_post_lesson_page_invalid_form(self):
        invalid_question = ''
        invalid_answer = ''

        lesson = Lesson.objects.get(pk=5)

        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.post(reverse('lesson:lesson_learn', kwargs={'theme_id': 5}),
                                  data={'question': invalid_question, 'answer': invalid_answer})

        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'lesson_learn.html')

        self.assertTrue(isinstance(result.context['form'], AddEditQuestionForm))
        self.assertEqual(result.context['lesson'], lesson)

    def test_get_edit_question_page(self):
        test_question_id = 20
        question = Question.objects.get(pk=20)

        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.get(reverse('lesson:edit_question', kwargs={'question_id': test_question_id}), data={})

        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'edit_question.html')
        self.assertEqual(result.context['question'], question)
        self.assertTrue(isinstance(result.context['form'], AddEditQuestionForm))

    def test_post_edit_question_page_valid_form(self):
        test_question_id = 20
        test_question = 'test_q_11'
        test_answer = 'test_a_11'

        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.post(reverse('lesson:edit_question',
                                          kwargs={'question_id': test_question_id}),
                                  data={'question': test_question, 'answer': test_answer})

        self.assertRedirects(result,
                             reverse('lesson:lesson_learn', kwargs={'theme_id': 5}),
                             fetch_redirect_response=False)

    def test_post_edit_question_page_invalid_form(self):
        test_question_id = 20
        invalid_question = ''
        invalid_answer = ''
        question = Question.objects.get(pk=20)
        lesson = Lesson.objects.get(pk=5)

        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.post(reverse('lesson:edit_question',
                                          kwargs={'question_id': test_question_id}),
                                  data={'question': invalid_question, 'answer': invalid_answer})

        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'lesson_learn.html')
        self.assertEqual(result.context['lesson'], lesson)
        self.assertTrue(isinstance(result.context['form'], AddEditQuestionForm))

    def test_get_delete_question_view(self):
        test_question_id = 20
        question = Question.objects.get(pk=20)

        login = self.client.login(username='TESTUSER', password='121212ab')

        result = self.client.get(reverse('lesson:delete_question', kwargs={'question_id': test_question_id}), data={})

        self.assertRedirects(result,
                             reverse('lesson:lesson_learn', kwargs={'theme_id': 5}),
                             fetch_redirect_response=False)
        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(pk=20)

