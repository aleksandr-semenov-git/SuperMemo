from datetime import date, timedelta
from random import randint
from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase

from lesson.services import QuestionService
from repeat.views import Repeat, RepeatCheck, Remember, NotRemember, RepeatMix


class RepeatViewsRepeatTest(SimpleTestCase):
    FILE_PATH = 'repeat.views.repeat'

    @patch(f'{FILE_PATH}.RepSessionService.get_rep_session_by_id')
    @patch(f'{FILE_PATH}.QuestionService.get_next_question_by_rep_session')
    @patch(f'{FILE_PATH}.render')
    def test_get_repeat_view_question_exists(self, patch_render, patch_get_question, patch_get_rep_session):
        test_rep_id = 1
        mock_rep_session = MagicMock()
        mock_question = MagicMock()
        mock_request = MagicMock()
        mock_http_result = MagicMock()

        patch_get_question.return_value = mock_question
        patch_get_rep_session.return_value = mock_rep_session
        patch_render.return_value = mock_http_result

        view = Repeat(request=mock_request)
        result = view.get(mock_request, test_rep_id)

        self.assertEqual(result, mock_http_result)
        patch_get_rep_session.assert_called_once_with(test_rep_id)
        patch_get_question.assert_called_once_with(mock_rep_session)
        patch_render.assert_called_once_with(mock_request, 'repeat.html', {'question': mock_question})

    @patch(f'{FILE_PATH}.RepSessionService.get_rep_session_by_id')
    @patch(f'{FILE_PATH}.QuestionService.get_next_question_by_rep_session')
    @patch(f'{FILE_PATH}.RepSessionService.finish_rep_session')
    @patch(f'{FILE_PATH}.redirect')
    def test_get_repeat_view_question_not_exists(
            self, patch_redirect, patch_finish, patch_get_question, patch_get_rep_session):
        test_rep_id = 1
        mock_rep_session = MagicMock()
        none_question = None
        mock_request = MagicMock()
        mock_http_result = MagicMock()

        patch_get_question.return_value = none_question
        patch_get_rep_session.return_value = mock_rep_session
        patch_redirect.return_value = mock_http_result
        patch_finish.return_value = mock_rep_session

        view = Repeat(request=mock_request)
        result = view.get(mock_request, test_rep_id)

        self.assertEqual(result, mock_http_result)
        patch_get_rep_session.assert_called_once_with(test_rep_id)
        patch_get_question.assert_called_once_with(mock_rep_session)
        patch_redirect.assert_called_once_with('account:profile_basic')
        patch_finish.assert_called_once_with(mock_rep_session)

    @patch(f'{FILE_PATH}.QuestionService.get_question_by_id')
    @patch(f'{FILE_PATH}.render')
    def test_get_repeat_check(self, patch_render, patch_get_question):
        test_question_id = 1
        mock_request = MagicMock()
        mock_http_result = MagicMock()
        mock_question = MagicMock()

        patch_get_question.return_value = mock_question
        patch_render.return_value = mock_http_result

        view = RepeatCheck(request=mock_request)
        result = view.get(mock_request, test_question_id)

        self.assertEqual(result, mock_http_result)
        patch_get_question.assert_called_once_with(test_question_id)

    @patch(f'{FILE_PATH}.QuestionService.get_question_by_id')
    @patch(f'{FILE_PATH}.RepSessionService.get_rep_session_in_progress')
    @patch(f'{FILE_PATH}.QStateService.get_qstate_by_q_id_and_rep_id')
    @patch(f'{FILE_PATH}.QuestionService.save_remembered_question')
    @patch(f'{FILE_PATH}.redirect')
    def test_post_remember_view(
            self, patch_redirect, patch_save, patch_get_qstate, patch_get_rep_session, patch_get_question):
        test_question_id = 1
        test_score = 2
        mock_request = MagicMock()
        mock_profile = MagicMock()
        mock_request.user.profile = mock_profile
        mock_http_result = MagicMock()
        mock_question = MagicMock()
        mock_rep_session = MagicMock()
        mock_qstate = MagicMock()

        patch_redirect.return_value = mock_http_result
        patch_save.return_value = mock_rep_session
        patch_get_qstate.return_value = mock_qstate
        mock_qstate.score = test_score
        patch_get_rep_session.return_value = mock_rep_session
        patch_get_question.return_value = mock_question

        view = Remember(request=mock_request)
        result = view.post(mock_request, test_question_id)

        self.assertEqual(result, mock_http_result)
        patch_redirect.assert_called_once_with('repeat:repeat', rep_id=mock_rep_session.id)
        patch_get_question.assert_called_once_with(test_question_id)
        patch_get_rep_session.assert_called_once_with(mock_profile)
        patch_get_qstate.assert_called_once_with(question_id=test_question_id, rep_id=mock_rep_session.id)
        patch_save.assert_called_once_with(mock_question, test_score)

    @patch(f'{FILE_PATH}.QuestionService.get_question_by_id')
    @patch(f'{FILE_PATH}.RepSessionService.get_rep_session_in_progress')
    @patch(f'{FILE_PATH}.QStateService.get_qstate_by_q_id_and_rep_id')
    @patch(f'{FILE_PATH}.QStateService.save_qstate_and_question')
    @patch(f'{FILE_PATH}.redirect')
    def test_post_not_remember_view(
            self, patch_redirect, patch_save, patch_get_qstate, patch_get_rep_session, patch_get_question):
        test_question_id = 1
        test_score = 2
        mock_request = MagicMock()
        mock_profile = MagicMock()
        mock_request.user.profile = mock_profile
        mock_http_result = MagicMock()
        mock_question = MagicMock()
        mock_rep_session = MagicMock()
        mock_qstate = MagicMock()

        patch_redirect.return_value = mock_http_result
        patch_get_qstate.return_value = mock_qstate
        mock_qstate.score = test_score
        patch_get_rep_session.return_value = mock_rep_session
        patch_get_question.return_value = mock_question

        view = NotRemember(request=mock_request)
        result = view.post(mock_request, test_question_id)

        self.assertEqual(result, mock_http_result)
        patch_redirect.assert_called_once_with('repeat:repeat', rep_id=mock_rep_session.id)
        patch_get_question.assert_called_once_with(test_question_id)
        patch_get_rep_session.assert_called_once_with(mock_profile)
        patch_get_qstate.assert_called_once_with(question_id=test_question_id, rep_id=mock_rep_session.id)
        patch_save.assert_called_once_with(qstate=mock_qstate, question=mock_question)

    @patch(f'{FILE_PATH}.RepSessionService.get_rep_session_in_progress')
    @patch(f'{FILE_PATH}.redirect')
    def test_get_repeat_mix_active_session_exists(
            self, patch_redirect, patch_get_rep_session):
        test_question_id = 1
        mock_request = MagicMock()
        mock_profile = MagicMock()
        mock_request.user.profile = mock_profile
        mock_http_result = MagicMock()
        mock_rep_session = MagicMock()

        patch_redirect.return_value = mock_http_result
        patch_get_rep_session.return_value = mock_rep_session

        view = RepeatMix(request=mock_request)
        result = view.get(mock_request, test_question_id)

        self.assertEqual(result, mock_http_result)
        patch_redirect.assert_called_once_with('repeat:repeat', rep_id=mock_rep_session.id)
        patch_get_rep_session.assert_called_once_with(mock_profile)

    @patch(f'{FILE_PATH}.RepSessionService.get_rep_session_in_progress')
    @patch(f'{FILE_PATH}.RepSessionService.create_mix_rep_session_in_progress')
    @patch(f'{FILE_PATH}.QuestionService.get_today_questions_by_profile')
    @patch(f'{FILE_PATH}.redirect')
    def test_get_repeat_mix_active_session_not_exists(
            self, patch_redirect, patch_get_questions, patch_create_session, patch_get_rep_session):
        test_question_id = 1
        test_rep_mod = 'M'
        mock_request = MagicMock()
        mock_profile = MagicMock()
        mock_questions = MagicMock()
        mock_request.user.profile = mock_profile
        mock_http_result = MagicMock()
        mock_rep_session = MagicMock()

        patch_get_rep_session.return_value = None
        patch_get_questions.return_value = mock_questions
        patch_create_session.return_value = mock_rep_session
        patch_redirect.return_value = mock_http_result

        view = RepeatMix(request=mock_request)
        result = view.get(mock_request, test_question_id)

        self.assertEqual(result, mock_http_result)
        patch_redirect.assert_called_once_with('repeat:repeat', rep_id=mock_rep_session.id)
        patch_get_rep_session.assert_called_once_with(mock_profile)
        patch_get_questions.assert_called_once_with(mock_profile)
        patch_create_session.assert_called_once_with(mock_profile, test_rep_mod, mock_questions)