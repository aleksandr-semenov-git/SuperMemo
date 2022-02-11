from datetime import date

from django.test import TestCase
from django.urls import reverse

from lesson.services import QuestionService
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