import csv
import os
from itertools import islice

from django.core.management.base import BaseCommand  # , CommandError

from reviews.models import (
    Category,
    CreatedUser,
    Comment,
    Genre,
    Title,
    Review
)


cwd = os.getcwd()
files = os.listdir(cwd)


class Command(BaseCommand):
    """Менеджмент команда для импорта csv."""
    help = 'Импорт баз данных из csv в SQLite.'

    def handle(self, *args, **kwargs):
        try:
            # Импорт comments.csv
            with open(
                'static/data/comments.csv',
                'r',
                newline=''
            ) as f:
                reader = csv.reader(f)
                for row in islice(reader, 1, None):
                    _, created = Comment.objects.get_or_create(
                        id=row[0],
                        review_id=int(row[1]),
                        text=row[2],
                        author_id=int(row[3]),
                        pub_date=row[4]
                    )
            self.stdout.write(
                self.style.SUCCESS(u'Импорт comments.csv завершён!'))
        except Exception as error:
            self.stdout.write(self.style.WARNING(error))
