from django.db import models

from app.models.agencies import Agency
from app.models.reports import Report
from app.models.schools import School
from app.models.users import User
from app.utils.helper import generateUniqueID


class SchoolReport(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.school.name} - {self.report.name}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generateUniqueID()
        super().save(*args, **kwargs)
