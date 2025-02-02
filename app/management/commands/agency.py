import json

from django.core.management.base import BaseCommand

import app.constants.config as CONFIG_CONSTANT
from app.models.agencies import Agency


class Command(BaseCommand):
    help = "Seed database with data from a JSON file"

    def handle(self, *args, **options):
        file_path = "./app/seeds/" + "Agency.json"

        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                for record in data:
                    record["access_school"] = record["access_school"] == "yes"
                    Agency.objects.create(**record)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully seeded database with {len(data)} records"
                    )
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error seeding database: {e}"))
