from django.db import models

import app.constants.options as OPTION_CONSTANT
from app.models.agencies import Agency
from app.utils.helper import generateUniqueID


class Report(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    report = models.CharField(max_length=200, blank=True)
    file_format = models.JSONField(default=list, blank=True)
    domain = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, blank=True, null=True)

    due_date = models.DateTimeField(blank=True, null=True)
    completion_time = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    content = models.JSONField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    video_cover = models.URLField(blank=True, null=True)
    file_urls = models.JSONField(default=list, blank=True)
    tag = models.CharField(max_length=50, blank=True, null=True)
    submission_format = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=OPTION_CONSTANT.REPORT_TYPE_CHOICES,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generateUniqueID()
        super().save(*args, **kwargs)
