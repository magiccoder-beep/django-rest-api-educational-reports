from django.contrib.postgres.fields import ArrayField
from django.db import models

from app.utils.helper import generateUniqueID


class Agency(models.Model):
    agency_title = models.CharField(max_length=255, primary_key=True)
    admin_privileges = ArrayField(
        models.CharField(max_length=100), blank=True, default=list
    )
    school_privileges = ArrayField(
        models.CharField(max_length=100), blank=True, default=list
    )
    access_school = models.BooleanField(default=False)
    home_url = models.URLField(blank=True, null=True)
    agency_unique_id = models.CharField(
        max_length=50, unique=True, blank=True, null=True
    )

    def __str__(self):
        return self.agency_title

    def save(self, *args, **kwargs):
        if not self.agency_unique_id:
            self.agency_unique_id = generateUniqueID()
        super().save(*args, **kwargs)
