from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", default='users\\default_user.png',
                              verbose_name='Фотография')
