from datetime import date

from django.db import models

from account.models import Profile


class QState(models.Model):
    """
    A class to save statistics of user's answers during learning process.

    Class attributes
    ----------------
    score : int
        major attribute that means how many tries user has got with the question
    rep_session : RepetitionSession
    question : Question
    """
    score = models.IntegerField(default=1)
    rep_session = models.ForeignKey('repeat.RepetitionSession',
                                    related_name='qstats',
                                    on_delete=models.SET_NULL,
                                    null=True)
    question = models.ForeignKey('lesson.Question', related_name='qstats', on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        self.question.save()
        super().save(*args, **kwargs)


class RepetitionSession(models.Model):
    """
    A class to store questions which were chosen to repeat by user

    Class attributes
    ----------------
    profile : Profile
    questions : models.ManyToManyField
    rep_mod : str
        this attribute shows which way of repeat user has preferred. Mix - all questions, Goal - all goal's questions...
    created_at : datetime
        control when session was started
    edited_at : datetime
        control when session was edited
    finished_at : date
        control when session was finished
    pause_started_at : date
        control when pause was started
    pause_stopped_at : date
        control when pause was finished
    is_started : bool
        control is session was started
    is_ended : bool
        control is session was ended
    is_paused : bool
        control is session was paused
    """
    MIX_MOD = 'M'
    GOAL_MOD = 'G'
    SECTION_MOD = 'S'
    THEME_MOD = 'T'
    MOD_CHOICES = (
        (MIX_MOD, 'Mix'),
        (GOAL_MOD, 'Goal'),
        (SECTION_MOD, 'Section'),
        (THEME_MOD, 'Theme'),
    )

    IN_PROGRESS = 'IP'
    FINISHED = 'F'
    PAUSED = 'P'
    STATUS_CHOICES = (
        (IN_PROGRESS, 'in progress'),
        (FINISHED, 'fin'),
        (PAUSED, 'paused'),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField('lesson.Question', through=QState, related_name='rep_sessions')
    rep_mod = models.CharField(choices=MOD_CHOICES, max_length=7, default=MIX_MOD)
    status = models.CharField(choices=STATUS_CHOICES, max_length=11, default=IN_PROGRESS)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateField(default=date.today)
    pause_started_at = models.DateTimeField(null=True)
    pause_stopped_at = models.DateTimeField(null=True)
