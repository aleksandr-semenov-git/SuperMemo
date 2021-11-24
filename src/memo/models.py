from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='user_images/%Y/%m/%d', default='user_images/default.jpg')


class Goal(models.Model):
    name = models.CharField(max_length=50, null=True)
    profile = models.ForeignKey(Profile, verbose_name='profile', related_name='goals', on_delete=models.CASCADE,
                                null=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=50, null=True)
    goal = models.ForeignKey(Goal, verbose_name='goal', related_name='sections', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Theme(models.Model):
    name = models.CharField(max_length=200, db_index=True, null=True)
    section = models.ForeignKey(Section, verbose_name='section', related_name='themes', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.IntegerField(default=1)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now=True)
    goal = models.ForeignKey(Goal, verbose_name='goal', related_name='lessons',  on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, verbose_name='profile', related_name='lessons',  on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    question = models.CharField(max_length=500, null=True)
    answer = models.CharField(max_length=500, null=True)
    lesson = models.ForeignKey(Lesson, verbose_name='lesson', related_name='questions', on_delete=models.CASCADE,
                               null=True)
    theme = models.ForeignKey(Theme, verbose_name='theme', related_name='questions', on_delete=models.CASCADE,
                              null=True)

    def __str__(self):
        return self.question
