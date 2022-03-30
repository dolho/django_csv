from django.db import models
from django.conf import settings
import datetime
import json
# Create your models here.


class Schema(models.Model):
    author_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50)
    separator = models.CharField(max_length=1)
    stringCharacter = models.CharField(max_length=1)
    columns = models.JSONField()
    modified = models.DateTimeField(default=datetime.datetime.now())


class DataSet(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)
    schema_id = models.ForeignKey(Schema, on_delete=models.DO_NOTHING)
    time_of_creation = models.DateTimeField(blank=True, null=True)
    path_to_file = models.URLField(blank=True, null=True)


