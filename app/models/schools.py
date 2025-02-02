import random
import time

from django.contrib.postgres.fields import ArrayField
from django.db import models

import app.constants.options as OPTION_CONSTANT
from app.models.agencies import Agency
from app.utils.helper import generateUniqueID


class School(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200, blank=False)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, blank=True, null=True)
    gradeserved = ArrayField(models.CharField(max_length=20), blank=True, default=list)
    county = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True, default="Pending")
    address = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=50, blank=False, null=True)
    logo = models.URLField(blank=True, null=True)
    number_lea = models.CharField(max_length=50, blank=True, null=True)
    creator = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f"{int(time.time() * 1000)}x{random.randint(100000000000000, 999999999999999)}"
        super().save(*args, **kwargs)


class SchoolDocument(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    file_url = models.CharField(max_length=255, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generateUniqueID()
        super().save(*args, **kwargs)
