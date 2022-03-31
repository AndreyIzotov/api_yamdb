import csv
import os
from itertools import islice

from django.core.management.base import BaseCommand  # , CommandError

from users.models import User


cwd = os.getcwd()
files = os.listdir(cwd)


class Command(BaseCommand):
    """Менеджмент команда для импорта csv."""
    help = 'Импорт баз данных из csv в SQLite.'

    def handle(self, *args, **kwargs):
        try:
            # Импорт users.csv
            with open(
                'static/data/users.csv',
                'r',
                newline=''
            ) as f:
                reader = csv.reader(f)
                for row in islice(reader, 1, None):
                    _, created = User.objects.get_or_create(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6]
                    )
            self.stdout.write(
                self.style.SUCCESS(u'Импорт users.csv завершён!'))
        except Exception as error:
            self.stdout.write(self.style.WARNING(error))
