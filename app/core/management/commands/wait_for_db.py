import time
from psycopg2 import OperationalError as Psycopg2Error  # type: ignore
from django.db.utils import OperationalError
from django.db import connections
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django management command to wait for the database to become available.
    Retries connection attempts with a timeout to avoid infinite waiting.
    """
    def handle(self, *args, **options):
        """Wait until the database is available."""
        self.stdout.write("Waiting for database...")
        max_attempts = 60  # 2 minuti di attesa massima (60 * 2 secondi)
        attempt = 1

        while attempt <= max_attempts:
            try:
                # Tenta di creare un cursore per il database 'default'
                connections['default'].cursor()
                self.stdout.write(self.style.SUCCESS(f"Database available after {attempt} attempt(s)!"))
                return
            except (Psycopg2Error, OperationalError) as e:
                self.stdout.write(
                    f"Database unavailable (attempt {attempt}/{max_attempts}): {str(e).splitlines()[0]}"
                )
                time.sleep(2)  # Aspetta 2 secondi prima di riprovare
                attempt += 1

        self.stdout.write(self.style.ERROR("Database connection failed after maximum attempts"))
        raise Exception("Failed to connect to the database after %d attempts" % max_attempts)