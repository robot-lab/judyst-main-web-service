from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    organization = models.TextField(blank=True)

    def __str__(self):
        return self.email
