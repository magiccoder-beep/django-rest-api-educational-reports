import json

from django.core.management.base import BaseCommand

import app.constants.config as CONFIG_CONSTANT
from app.models.agencies import Agency
from app.models.applications import Application


class Command(BaseCommand):
    help = "Seed database with data from a JSON file"

    def handle(self, *args, **options):
        file_path = "./app/seeds/" + "Application.json"

        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                for record in data:

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
                    Application.objects.create(**record)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully seeded database with {len(data)} records"
                    )
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error seeding database: {e}"))
