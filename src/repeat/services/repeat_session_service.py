from datetime import date

from django.db.models import QuerySet

from account.models import Profile
from repeat.models import RepetitionSession, QState


class RepSessionService:
    @staticmethod
    def get_rep_session_by_id(rep_id: int) -> RepetitionSession:
        rep_session = RepetitionSession.objects.get(id=rep_id)
        return rep_session

    @staticmethod
    def find_all_started_rep_sessions(profile: Profile) -> QuerySet:
        active_rep_session_query = RepetitionSession.objects.filter(profile=profile,
                                                                    is_started=True,
                                                                    is_ended=False)
        return active_rep_session_query

    @staticmethod
    def look_for_rep_session(active_rep_session_query: QuerySet) -> RepetitionSession or False or Exception:
        """Check profile for multiple and empty rep sessions

        raise exception for multiple rep sessions,
        delete empty rep session

        parameters:
            active_rep_session_query -- queryset
        return values:
            return raise due to exception
            return False if rep_session is not exist
            return rep_session if all good
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
        rep_session.is_ended = True
        rep_session.finished_at = date.today()
        rep_session.save()

    @staticmethod
    def get_or_create_rep_session_goal():
        rep_session = RepetitionSession.objects.get_or_create()
        return rep_session

    @staticmethod
    def get_or_create_rep_session_section():
        rep_session = RepetitionSession.objects.get_or_create()
        return rep_session

    @staticmethod
    def get_or_create_rep_session_theme():
        rep_session = RepetitionSession.objects.get_or_create()
        return rep_session
