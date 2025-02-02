import json

from django.core.management.base import BaseCommand

import app.constants.config as CONFIG_CONSTANT
from app.models.agencies import Agency
from app.models.reports import Report


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = "./app/seeds/" + "Report.json"
        count = 0
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                for record in data:
                    count += 1
                    if "agency" in record and record["agency"] != "":
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
                    if "agency" in record and not record["agency"]:
                        record["agency"] = None
                    Report.objects.create(**record)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error seeding database: {e}"))
