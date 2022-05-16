from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """ user class to register and save users"""
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email