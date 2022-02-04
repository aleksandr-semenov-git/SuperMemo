from datetime import date

from django.db import models

from memo.models import Goal


class Section(models.Model):
    """
    This is models.Model class. Class which used for separating user's goals on sections.

    Class attributes
    ----------------
    name : str
    goal : models.ForeignKey

    Methods
    -------
    __str__(self):
        return Section's name
    """
    name = models.CharField(max_length=50, null=True)
    goal = models.ForeignKey(Goal, verbose_name='goal', related_name='sections', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Theme(models.Model):
    """
    This is models.Model class. Class which used for separating user's sections on themes.

    Class attributes
    ----------------
    name : str
    section : models.ForeignKey

    Methods
    -------
    __str__(self):
        return Theme's name
    """
    name = models.CharField(max_length=200, db_index=True, null=True)
    section = models.ForeignKey(Section,
                                verbose_name='section',
                                related_name='themes',
                                on_delete=models.CASCADE,
                                null=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    This is models.Model class. Class which used for storing user's questions in sorted way.

    Class attributes
    ----------------
    name : str
        Lesson's name is built from Goal's, Section's, Theme's names
    goal : models.ForeignKey
    theme : models.OneToOneField

    Methods
    -------
    __str__(self):
        return Lesson's name
    """
    name = models.CharField(max_length=250, null=True)
    goal = models.ForeignKey(Goal, verbose_name='goal', related_name='lessons',  on_delete=models.CASCADE, null=True)
    theme = models.OneToOneField(Theme, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    """
    This is models.Model class. Class which used for storing information about user's questions.

    Class attributes
    ----------------
    question : str
    answer : str
    lesson : models.ForeignKey
    created_at : datetime
        time when question was created
    edited_at : datetime
        time when question was edited
    prev_repeat_at : date
        previous repetition date of the question
    next_repeat_at : date
        next repetition date of the question
    cycle : int
        parameter which determine number of days user can not repeat the question
    memo_index : decimal
        special coefficient which is used for calculating question's cycle. NOT USED IN THIS VERSION
    repeated_num : int
        store statistics about number of repetitions of the question

    Methods
    -------
    __str__(self):
        return Question's question
    """
    question = models.CharField(max_length=500, null=True)
    answer = models.CharField(max_length=500, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, verbose_name='lesson', related_name='questions', on_delete=models.CASCADE,
                               null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    prev_repeat_at = models.DateField(default=date.today)
    next_repeat_at = models.DateField(default=date.today)
    cycle = models.PositiveIntegerField(default=0)
    memo_index = models.DecimalField(null=True, decimal_places=2, default=1.00, max_digits=4)

    repeated_num = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.question
