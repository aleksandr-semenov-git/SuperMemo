from datetime import date

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
    MIX = 'M'
    GOAL = 'G'
    SECTION = 'S'
    THEME = 'T'
    MOD_CHOICES = (
        (MIX, 'Mix'),
        (GOAL, 'Goal'),
        (SECTION, 'Section'),
        (THEME, 'Theme'),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField('lesson.Question', through=QState, related_name='rep_sessions')
    rep_mod = models.CharField(choices=MOD_CHOICES, max_length=7, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateField(default=date.today)
    pause_started_at = models.DateTimeField(null=True)
    pause_stopped_at = models.DateTimeField(null=True)

    is_started = models.BooleanField(default=False)
    is_ended = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
