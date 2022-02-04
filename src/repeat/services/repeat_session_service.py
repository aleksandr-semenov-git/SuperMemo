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
        rep_session = RepetitionSession.objects.get(id=rep_id)
        return rep_session

    @staticmethod
    def get_rep_session_in_progress(profile):
        try:
            active_rep_session = RepetitionSession.objects.get(profile=profile, status=RepetitionSession.IN_PROGRESS)
            return active_rep_session
        except:
            active_rep_session_query = RepetitionSession.objects.filter(profile=profile,
                                                                        status=RepetitionSession.IN_PROGRESS)
            for session in active_rep_session_query:
                RepSessionService.finish_rep_session(session)
            return None

    @staticmethod
    def create_rep_session(profile, rep_mod, questions) -> RepetitionSession:
        """"""
        rep_session, created = RepetitionSession.objects.get_or_create(profile=profile,
                                                                       rep_mod=rep_mod,
                                                                       status=RepetitionSession.IN_PROGRESS)
        for question in questions:
            QState.objects.get_or_create(rep_session=rep_session, question=question)
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
