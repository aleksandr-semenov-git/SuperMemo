from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Class which used for storing user's photo and mind map

    Class attributes
    ----------------
    user : models.OneToOneField
    photo : models.ImageField
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='user_images/%Y/%m/%d', default='user_images/default.jpg')
