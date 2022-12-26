from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from lesson.models import Question
from lesson.services import QuestionService
from repeat.models import RepetitionSession
from repeat.services import RepSessionService


class RepeatPagesTest(TestCase):
    fixtures = ['lesson_repeat_fixtures.json']

    def test_get_repeat_view_next_question_exists(self):
        test_rep_id = 17
        expected_rep_session = RepSessionService.get_rep_session_by_id(test_rep_id)
        expected_next_question = expected_rep_session.questions.first()
        expected_next_question.next_repeat_at = date.today()
        expected_next_question.save()
        expected_next_question = QuestionService.get_next_question_by_rep_session(expected_rep_session)

        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.get(reverse('repeat:repeat', kwargs={'rep_id': test_rep_id}))

        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'repeat.html')
        self.assertEqual(result.context['question'], expected_next_question)

    def test_get_repeat_view_next_question_not_exists(self):
        test_rep_id = 16
        expected_rep_session = RepSessionService.get_rep_session_by_id(test_rep_id)
        expected_rep_session.status = RepetitionSession.IN_PROGRESS
        questions = expected_rep_session.questions.all()
        for question in questions:
            question.next_repeat_at = date.today() + timedelta(days=1)
        Question.objects.bulk_update(questions, ['next_repeat_at'])

        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.get(reverse('repeat:repeat', kwargs={'rep_id': test_rep_id}))

        self.assertRedirects(
            result, '/account/profile/', status_code=302, target_status_code=302, fetch_redirect_response=True)

    def test_get_repeatcheck_view(self):
        test_q_id = 13
        expected_question = QuestionService.get_question_by_id(test_q_id)

        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.get(reverse('repeat:repeat_check', kwargs={'question_id': test_q_id}))

        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'repeat_check.html')
        self.assertEqual(result.context['question'], expected_question)

    def test_post_remember_view(self):
        test_q_id = 13
        test_rep_id = 16
        expected_rep_session = RepSessionService.get_rep_session_by_id(test_rep_id)
        expected_rep_session.status = RepetitionSession.IN_PROGRESS
        expected_rep_session.save()

        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.post(reverse('repeat:remember', kwargs={'question_id': test_q_id}))

        self.assertRedirects(
            result, f'/repeat/{test_rep_id}/', status_code=302, fetch_redirect_response=False)

    def test_post_notremember_view(self):
        test_q_id = 13
        test_rep_id = 16
        expected_rep_session = RepSessionService.get_rep_session_by_id(test_rep_id)
        expected_rep_session.status = RepetitionSession.IN_PROGRESS
        expected_rep_session.save()

        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.post(reverse('repeat:not_remember', kwargs={'question_id': test_q_id}))

        self.assertRedirects(
            result, f'/repeat/{test_rep_id}/', status_code=302, fetch_redirect_response=False)

    def test_get_repeatmix_view_active_session_exists(self):
        test_q_id = 13
        test_rep_id = 16
        expected_rep_session = RepSessionService.get_rep_session_by_id(test_rep_id)
        expected_rep_session.status = RepetitionSession.IN_PROGRESS
        expected_rep_session.save()
        expected_next_question = expected_rep_session.questions.first()
        expected_next_question.next_repeat_at = date.today()
        expected_next_question.save()

        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.get(reverse('repeat:repeat_mix'))

        self.assertRedirects(
            result, f'/repeat/{test_rep_id}/', status_code=302, fetch_redirect_response=False)

    def test_get_repeatmix_view_active_session_not_exists(self):
        expected_rep_session_number = RepetitionSession.objects.all().count() + 1
        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.get(reverse('repeat:repeat_mix'))

        self.assertEqual(result.status_code, 302)
        self.assertEqual(RepetitionSession.objects.all().count(), expected_rep_session_number)