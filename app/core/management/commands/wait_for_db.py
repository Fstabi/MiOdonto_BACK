# Django command to wait for the db to be available

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    # This command will wait for the database to be available before running any other commands.
    
    def handle(self, *args, **options):
        pass