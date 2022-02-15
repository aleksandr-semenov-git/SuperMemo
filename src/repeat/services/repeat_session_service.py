from datetime import date

from repeat.models import RepetitionSession, QState


class RepSessionService:
    @staticmethod
    def get_rep_session_by_id(rep_id: int) -> RepetitionSession:
        """
        Parameters
        ----------
        rep_id : int

        Returns
        -------
        rep_session : RepetitionSession
        """
        rep_session = RepetitionSession.objects.get(pk=rep_id)
        return rep_session

    @staticmethod
    def get_rep_session_in_progress(profile):
        active_rep_session = RepetitionSession.objects.filter(
            profile=profile, status=RepetitionSession.IN_PROGRESS).first()
        return active_rep_session

    @staticmethod
    def create_mix_rep_session_in_progress(profile, rep_mod, questions) -> RepetitionSession:
        """"""
        rep_session = RepetitionSession.objects.create(profile=profile,
                                                       rep_mod=rep_mod,
                                                       status=RepetitionSession.IN_PROGRESS)
        qstate_list = []
        for question in questions:
            qstate_list.append(QState(rep_session=rep_session, question=question))
        QState.objects.bulk_create(qstate_list)
        return rep_session

    @staticmethod
    def finish_rep_session(rep_session):
        """Finish rep_session. Put is_ended attribute to True, save finished_at date, save rep_session and return it"""
        rep_session.status = RepetitionSession.FINISHED
        rep_session.finished_at = date.today()
        rep_session.save()
        return rep_session

    @staticmethod
    def get_or_create_rep_session_goal():
        # Todo: in progress
        rep_session = RepetitionSession.objects.get_or_create()
        return rep_session

    @staticmethod
    def get_or_create_rep_session_section():
        # Todo: in progress
        rep_session = RepetitionSession.objects.get_or_create()
        return rep_session

    @staticmethod
    def get_or_create_rep_session_theme():
        # Todo: in progress
        rep_session = RepetitionSession.objects.get_or_create()
        return rep_session
