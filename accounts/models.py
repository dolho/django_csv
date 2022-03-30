from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_regular_account = models.BooleanField(default=True)
    # add additional fields in here

    def __str__(self):
        return self.username


