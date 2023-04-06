from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phonenumber = models.CharField(max_length=14)
    email = models.EmailField(unique=True, max_length=250)
  

    def __str__(self):
        return self.email
