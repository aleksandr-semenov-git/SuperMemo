from django.test import TestCase
from django.urls import reverse

from lesson.forms import AddEditQuestionForm
from lesson.models import Lesson, Question
from lesson.services import QuestionService
from repeat.models import QState, RepetitionSession
from repeat.services import RepSessionService


class RepeatPagesTest(TestCase):
    fixtures = ['lesson_repeat_fixtures.json']

    def test_get_repeat_view(self):
        test_rep_id = 19
        expected_rep_session = RepSessionService.get_rep_session_by_id(test_rep_id)
        expected_next_question = QuestionService.get_next_question_by_rep_session(expected_rep_session)

        login = self.client.login(username='TESTUSER', password='121212ab')
        result = self.client.get(reverse('repeat:repeat'))
