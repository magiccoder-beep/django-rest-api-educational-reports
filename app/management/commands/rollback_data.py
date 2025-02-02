from django.core.management.base import BaseCommand

from app.models.agencies import Agency
from app.models.complaints import Complaint
from app.models.reports import Report
from app.models.schools import School
from app.models.submissions import Submission
from app.models.users import User


class Command(BaseCommand):
    help = "Rollback seeded data from the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Rolling back seeded data...")

        # Delete data from models
        User.objects.all().delete()
        # Report.objects.all().delete()
        # Submission.objects.all().delete()
        # School.objects.all().delete()
        # Agency.objects.all().delete()
        # Complaint.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Rollback completed successfully!"))
