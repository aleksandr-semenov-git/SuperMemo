from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='user_images/%Y/%m/%d', default='user_images/default.jpg')


class Goal(models.Model):
    name = models.CharField(max_length=50, null=True)
    profile = models.ForeignKey(Profile, verbose_name='profile', related_name='goals', on_delete=models.CASCADE,
                                null=True)

    def __str__(self):
        return self.name


