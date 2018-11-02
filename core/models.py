from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models


# Magic numbers take from magic specifications.
class CustomUser(AbstractUser):
    first_name = models.CharField(blank=True, max_length=255)
    last_name = models.CharField(blank=True, max_length=255)
    organization = models.CharField(blank=True, max_length=255)
    verificate = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.email


class Documents(models.Model):
    doc_id = models.TextField(primary_key=True, blank=False, )
    super_type = models.TextField()
    release_date = models.TextField()
    doc_type = models.TextField()
    title = models.TextField()
    text_source_url = models.URLField()
    text = models.TextField()


class Links(models.Model):
    doc_id_from = models.TextField(blank=False, null=False)
    doc_fk = models.ForeignKey(to=Documents, null=True, blank=True,
                               on_delete=models.CASCADE, related_name='links_for_doc')
    doc_id_to = models.TextField(blank=False, null=False)
    to_doc_title = models.TextField()
    citations_number = models.IntegerField()
    positions_list = ArrayField(models.TextField(blank=True), blank=True)
    """
    positions_list - массив строк где лежат строки после json.dumps(dict)"""
