from django.db import models
from account.models import Profile


class Goal(models.Model):
    name = models.CharField(max_length=50, null=True)
    profile = models.ForeignKey(Profile, verbose_name='profile', related_name='goals', on_delete=models.CASCADE,
                                null=True)

    def __str__(self):
        return self.name
