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



