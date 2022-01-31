from django.db.models import QuerySet
from datetime import datetime
from repeat.models import RepetitionSession, QState
from account.models import Profile


class QStateService:
    @staticmethod
    def get_qstate_by_q_id_and_rep_id(question_id, rep_session_id: int) -> QState:
        qstate = QState.objects.get(question__id=question_id, rep_session__id=rep_session_id)
        return qstate
