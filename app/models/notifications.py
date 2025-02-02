from django.db import models

import app.constants.options as OPTION_CONSTANT
from app.utils.helper import generateUniqueID

class Notification(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    receiver = models.CharField(max_length=50, blank=True, null=True)
    read = models.BooleanField(default=False)
    type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generateUniqueID()
        super().save(*args, **kwargs)