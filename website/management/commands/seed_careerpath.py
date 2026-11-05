from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Populate the CareerPath database with starter data for roadmaps, careers, courses, scholarships, exams, and team placeholders."

    def handle(self, *args, **options):
        call_command("seed_data")
