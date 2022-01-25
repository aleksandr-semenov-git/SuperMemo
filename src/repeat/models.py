from django.db import models
from account.models import Profile


class QState(models.Model):
    score = models.IntegerField(default=1)
    rep_session = models.ForeignKey('repeat.RepetitionSession',
                                    related_name='qstats',
                                    on_delete=models.SET_NULL,
                                    null=True)
    question = models.ForeignKey('lesson.Question', related_name='qstats', on_delete=models.SET_NULL, null=True)


class RepetitionSession(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField('lesson.Question', through=QState, related_name='rep_sessions')

    start_at = models.DateTimeField(null=True)
    finish_at = models.DateTimeField(null=True)
    pause_started_at = models.DateTimeField(null=True)
    pause_stopped_at = models.DateTimeField(null=True)

    is_started = models.BooleanField(default=False)
    is_ended = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)

