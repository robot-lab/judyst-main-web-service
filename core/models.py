from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


class CustomUser(AbstractUser):
    # Magic numbers take from magic specifications.
    first_name = models.CharField(blank=True, max_length=255)
    last_name = models.CharField(blank=True, max_length=255)
    organization = models.CharField(blank=True, max_length=255)
    verificate = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Links(models.Model):
    doc_id_from = models.TextField(blank=False, null=False)
    doc_id_to = models.TextField(blank=False, null=False)
    to_doc_title = models.TextField()
    citations_number = models.IntegerField()
    contexts_list = ArrayField(models.TextField())
    positions_list = ArrayField(models.IntegerField())
