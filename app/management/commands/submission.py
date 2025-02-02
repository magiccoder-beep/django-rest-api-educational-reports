import json

from django.core.management.base import BaseCommand

import app.constants.config as CONFIG_CONSTANT
from app.models.agencies import Agency
from app.models.reports import Report
from app.models.schools import School
from app.models.submissions import Submission
from app.models.users import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = "./app/seeds/" + "Submission.json"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                for record in data:
                    flag = True
                    if (
                        not record["agency"]
                        or not record["school"]
                        or not record["report"]
                    ):
                        continue
                    if record["agency"] != "":
                        try:
                            record["agency"] = Agency.objects.get(
                                agency_title=record["agency"]
                            )
                        except Agency.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Agency '{
                                        record['agency']}' not found. Skipping record."
                                )
                            )
                            continue
                    if record["school"] != "":
                        try:
                            record["school"] = School.objects.get(id=record["school"])
                        except School.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"School '{
                                        record['school']}' not found. Skipping record."
                                )
                            )
                            continue
                    if record["report"] != "":
                        try:
                            record["report"] = Report.objects.get(id=record["report"])
                        except Report.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Report '{
                                        record['report']}' not found. Skipping record."
                                )
                            )
                            continue
                    if record["assigned_member"] != "":
                        try:
                            record["assigned_member"] = User.objects.get(
                                id=record["assigned_member"]
                            )
                        except User.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Assigned Member '{
                                        record['assigned_member']}' not found. Skipping record."
                                )
                            )
                            record["assigned_member"] = None
                    if record["assigned_member"] == "":
                        record["assigned_member"] = None
                    Submission.objects.create(**record)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error seeding database: {e}"))
