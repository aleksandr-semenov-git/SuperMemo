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

