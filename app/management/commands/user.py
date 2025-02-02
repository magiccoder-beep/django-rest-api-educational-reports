import json

from django.core.management.base import BaseCommand

import app.constants.config as CONFIG_CONSTANT
from app.models.agencies import Agency
from app.models.schools import School
from app.models.users import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = "./app/seeds/" + "User.json"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                for record in data:
                    record["username"] = record["email"]
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
                    if not record["agency"]:
                        record["agency"] = None
                    if not record["school"]:
                        record["school"] = None
                    User.objects.create(**record)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error seeding database: {e}"))
