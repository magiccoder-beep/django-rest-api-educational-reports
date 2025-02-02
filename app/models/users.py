import random
import time

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import JSONField

from app.models.agencies import Agency
from app.models.schools import School


class User(AbstractUser):

    id = models.CharField(max_length=50, primary_key=True)
    email = models.CharField(max_length=100, unique=True, blank=True, null=True)
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.URLField(max_length=200, blank=True, null=True)
    role = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=20, default="Member")
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)
    notification_settings = JSONField(default=dict)

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f"{int(time.time() * 1000)}x{random.randint(100000000000000, 999999999999999)}"
        super().save(*args, **kwargs)
