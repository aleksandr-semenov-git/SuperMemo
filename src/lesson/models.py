from django.db import models
from memo.models import Goal


class Section(models.Model):
    name = models.CharField(max_length=50, null=True)
    goal = models.ForeignKey(Goal, verbose_name='goal', related_name='sections', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(max_length=200, db_index=True, null=True)
    section = models.ForeignKey(Section,
                                verbose_name='section',
                                related_name='themes',
                                on_delete=models.CASCADE,
                                null=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=250, null=True)
    goal = models.ForeignKey(Goal, verbose_name='goal', related_name='lessons',  on_delete=models.CASCADE, null=True)
    theme = models.OneToOneField(Theme, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    question = models.CharField(max_length=500, null=True)
    answer = models.CharField(max_length=500, null=True)
    lesson = models.ForeignKey(Lesson, verbose_name='lesson', related_name='questions', on_delete=models.CASCADE,
                               null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    score = models.FloatField(null=True)
    repeated_count = models.IntegerField(null=True)
    repeated_count_in_last_cycle = models.IntegerField(null=True)

    def __str__(self):
        return self.question
