from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models


# Magic numbers take from magic specifications.
class CustomUser(AbstractUser):
    first_name = models.CharField(blank=True, max_length=255)
    last_name = models.CharField(blank=True, max_length=255)
    organization = models.CharField(blank=True, max_length=255)
    verification = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.email


class Documents(models.Model):
    doc_id = models.TextField(unique=True, blank=False)
    supertype = models.TextField(blank=False)
    doc_type = models.TextField(blank=False)
    title = models.TextField(blank=False)
    release_date = models.DateField(blank=False)
    text = models.TextField()
    text_source_url = models.TextField(blank=False)
    effective_date = models.DateField()
    absolute_path = models.TextField()
    interredaction_id = models.TextField()
    # i suppose to leave this field as text and store here json, for beginning
    cons_selected_info = models.TextField()


class Links(models.Model):
    doc_id_from = models.TextField(blank=False, null=False)
    doc_fk = models.ForeignKey(to=Documents, null=True, blank=True,
                               on_delete=models.CASCADE, related_name='links_for_doc')
    doc_id_to = models.TextField(blank=False, null=False)
    citations_number = models.IntegerField()
    positions_list = ArrayField(models.TextField(blank=True), blank=True)
    """
    positions_list - массив строк где лежат строки после json.dumps(dict)"""
