from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Magic numbers take from magic specifications.
    first_name = models.CharField(blank=True, max_length=255)
    last_name = models.CharField(blank=True, max_length=255)
    organization = models.CharField(blank=True, max_length=1024)
    verificate = models.BooleanField(default=False)

    def __str__(self):
        return self.email
