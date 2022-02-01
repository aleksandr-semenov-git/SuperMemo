from datetime import date

from django.db.models import QuerySet

from account.models import Profile
from repeat.models import RepetitionSession, QState


class RepSessionService:
    @staticmethod
    def get_rep_session_by_id(rep_id: int) -> RepetitionSession:
        """Take rep_id, return rep_session"""
        rep_session = RepetitionSession.objects.get(id=rep_id)
        return rep_session

    @staticmethod
    def find_all_started_rep_sessions(profile: Profile) -> QuerySet:
        """Get profile, return filtered queryset with all started rep_sessions"""
        active_rep_session_query = RepetitionSession.objects.filter(profile=profile,
                                                                    is_started=True,
                                                                    is_ended=False)
        return active_rep_session_query

    @staticmethod
    def look_for_rep_session(active_rep_session_query: QuerySet) -> RepetitionSession or False or Exception:
        """Get rep_session and check db for bugs connected to user's rep_sessions.

        Raise exception if multiple rep sessions exist in the profile.
        Delete empty rep session if it exist.
        Get rep_session object from active_rep_session_query if all OK.
            Parameters:
                active_rep_session_query (QuerySet): queryset which consist of rep_session
            Returns:
                Exception (Exception): raise exception if bug detected
                False (bool): if rep_session is not exist
                rep_session (RepetitionSession): if all good
        """
        query_len = len(active_rep_session_query)
        if query_len > 1:
            print('EXCEPTION. THERE ARE MORE THAN 1 ACTIVE SESSIONS')
            # Todo: Exception
        elif query_len == 1:
            rep_session = active_rep_session_query[0]
            # check is rep_session empty for no reason
            if len(rep_session.questions.all()) == 0:
                rep_session.delete()
                return False
            else:
                return rep_session
        else:
            return False

    @staticmethod
    def get_or_create_rep_session_mix(profile, questions, rep_mod='M') -> (RepetitionSession, str):
        """Get rep_session and check db for bugs connected to user's rep_sessions.

        Find active_rep_session and change rep_mod to 'active_rep_exists'.
        If active_rep_session not exist create new one through the QState objects which connected to every question.
            Parameters:
                profile (Profile): user's profile
                questions (QuerySet or None): today's question
                rep_mod (str): RepetitionSession's attribute and also message, which using to control rep_sessions
            Returns:
                tuple (RepetitionSession, str): return rep_session and rep_mod
        """
        active_rep_session_query = RepSessionService.find_all_started_rep_sessions(profile)
        active_rep_session = RepSessionService.look_for_rep_session(active_rep_session_query)

        if active_rep_session:
            rep_mod = 'active_rep_exists'
            return active_rep_session, rep_mod
        else:
            rep_session = RepetitionSession.objects.create(profile=profile,
                                                           rep_mod=rep_mod,
                                                           is_started=True)
            for question in questions:
                QState.objects.create(rep_session=rep_session, question=question)
            return rep_session, rep_mod

    @staticmethod
    def finish_rep_session(rep_session):
        """Finish rep_session. Put is_ended attribute to True, save finished_at date, save rep_session and return it"""
        rep_session.is_ended = True
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
