from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase

from repeat.services import QStateService


class QStateServiceTest(SimpleTestCase):
    FILE_PATH = 'repeat.services.qstate_service'

    @patch(f'{FILE_PATH}.QState.objects.get')
    def test_get_qstate_by_q_id_and_rep_id(self, patch_qstate_get):
        test_q_id = 1
        test_rep_id = 2
        qstate = MagicMock()
        patch_qstate_get.return_value = qstate
        result = QStateService.get_qstate_by_q_id_and_rep_id(question_id=test_q_id, rep_id=test_rep_id)
        patch_qstate_get.assert_called_once_with(question__id=test_q_id, rep_session__id=test_rep_id)
        self.assertEqual(qstate, result)

    def test_save_qstate_and_question(self):
        expected_score = 2
        mock_qstate = MagicMock(score=1)
        mock_question = MagicMock()

        result = QStateService.save_qstate_and_question(mock_qstate, mock_question)
        mock_qstate.save.assert_called_once()
        self.assertEqual(mock_qstate.score, expected_score)
