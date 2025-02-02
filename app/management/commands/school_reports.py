import json

from django.core.management.base import BaseCommand

import app.constants.config as CONFIG_CONSTANT
from app.models.agencies import Agency
from app.models.reports import Report
from app.models.school_reports import SchoolReport
from app.models.schools import School
from app.models.users import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = "./app/seeds/" + "School-Report.json"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                total_records = len(data)  # Total number of records
                completed_records = 0

                for index, record in enumerate(data, start=1):
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

                    SchoolReport.objects.create(**record)
                    completed_records += 1

                    # Calculate and display progress percentage
                    progress = (index / total_records) * 100
                    self.stdout.write(
                        f"\rProgress: {progress:.2f}% ({index}/{total_records})",
                        ending="",
                    )

                self.stdout.write("\nSeeding completed successfully.")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error seeding database: {e}"))
