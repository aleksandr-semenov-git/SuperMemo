from django.db import models
from account.models import Profile


class Goal(models.Model):
    """
    Class which used for determining user's purposes.

    Class attributes
    ----------------
    name : str
    profile : models.ForeignKey

    Methods
    -------
    __str__(self):
        return Goal's name
    """
    name = models.CharField(max_length=150, null=True)
    profile = models.ForeignKey(Profile, verbose_name='profile', related_name='goals', on_delete=models.CASCADE,
                                null=True)

    def __str__(self):
        return self.name
