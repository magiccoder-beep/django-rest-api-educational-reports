# myapp/management/commands/run_commands.py
import subprocess
import time

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Runs a series of commands one by one"

    def handle(self, *args, **kwargs):
        commands = [
            "python manage.py agency",
            "python manage.py school",
            "python manage.py user",
            "python manage.py report",
            "python manage.py application",
            "python manage.py submission",
            "python manage.py school_reports",
        ]

        for i, command in enumerate(commands, 1):
            self.stdout.write(f"Running command {i}: {command}")
            self.run_command(command)

    def run_command(self, command):
        """Helper function to run each command and handle errors."""
        try:
            result = subprocess.run(
                command, shell=True, check=True, capture_output=True
            )
            self.stdout.write(f"Output of {command}:\n{result.stdout.decode()}")
            self.stderr.write(f"Errors (if any): {result.stderr.decode()}")
        except subprocess.CalledProcessError as e:
            self.stderr.write(
                f"Command '{command}' failed with error:\n{e.stderr.decode()}"
            )
