from unittest.mock import patch, MagicMock, call

from django.test import SimpleTestCase

from repeat.models import RepetitionSession
from repeat.services import RepSessionService


class RepSessionServiceTest(SimpleTestCase):
    FILE_PATH = 'repeat.services.repeat_session_service'

    @patch(f'{FILE_PATH}.RepetitionSession.objects.get')
    def test_get_qstate_by_q_id_and_rep_id(self, patch_rep_session_get):
        test_rep_session = MagicMock()
        test_rep_id = 1
        patch_rep_session_get.return_value = test_rep_session
        result = RepSessionService.get_rep_session_by_id(test_rep_id)
        patch_rep_session_get.assert_called_once_with(pk=test_rep_id)
        self.assertEqual(result, test_rep_session)

    @patch(f'{FILE_PATH}.RepetitionSession.objects.filter')
    def test_get_rep_session_in_progress(self, patch_rep_session_filter):
        expected_status = RepetitionSession.IN_PROGRESS
        test_rep_session = MagicMock()
        test_profile = MagicMock()
        patch_rep_session_filter.return_value = test_rep_session
        test_rep_session.first.return_value = test_rep_session
        result = RepSessionService.get_rep_session_in_progress(test_profile)
        patch_rep_session_filter.assert_called_once_with(profile=test_profile, status=expected_status)
        test_rep_session.first.assert_called_once()
        self.assertEqual(result, test_rep_session)

    @patch(f'{FILE_PATH}.RepetitionSession.objects.create')
    @patch(f'{FILE_PATH}.QState.objects.bulk_create')
    @patch(f'{FILE_PATH}.QState')
    def test_create_mix_rep_session_in_progress(self, patch_qstate_model, patch_bulk_create, patch_create_rep_session):
        test_profile = MagicMock()
        test_rep_session = MagicMock()
        test_q1 = MagicMock()
        test_q2 = MagicMock()
        test_qstate = MagicMock()
        test_questions = [test_q1, test_q2]
        test_status = RepetitionSession.IN_PROGRESS
        test_mod = 'MIX'
        mock_qstate1 = MagicMock()
        mock_qstate2 = MagicMock()

        patch_qstate_model.side_effect = [mock_qstate1, mock_qstate2]
        patch_qstate_model.return_value = test_qstate
        patch_create_rep_session.return_value = test_rep_session

        result = RepSessionService.create_mix_rep_session_in_progress(test_profile, test_mod, test_questions)

        patch_create_rep_session.assert_called_once_with(profile=test_profile, rep_mod=test_mod, status=test_status)
        patch_qstate_model.assert_has_calls([call(rep_session=test_rep_session, question=test_q1),
                                      call(rep_session=test_rep_session, question=test_q2)])

        patch_bulk_create.assert_called_once_with([mock_qstate1, mock_qstate2])
        self.assertEqual(result, test_rep_session)

    @patch(f'{FILE_PATH}.date')
    def test_finish_rep_session(self, patch_date):
        mock_date = MagicMock()
        patch_date.return_value = mock_date
        mock_date.today.return_value = mock_date
        test_rep_session = MagicMock()
        result = RepSessionService.finish_rep_session(test_rep_session)
        self.assertEqual(result, test_rep_session)
        self.assertEqual(result.finished_at, mock_date)
        self.assertEqual(result.status, 'F')
