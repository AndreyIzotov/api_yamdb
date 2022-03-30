import csv

from django.core.management.base import BaseCommand, CommandError

from reviews.models import Review, Comment

class Command(BaseCommand):
    """Менджмент команда для импорта csv."""
    help = 'Импорт баз данных из csv в SQLite.'

    with open(
        'static/data/comments.csv',
        'r',
        # newline=''
    ) as f:
        reader = csv.reader(f)
        for row in reader:
            _, created = Comment.objects.get_or_create(
                id=row[0],
                review_id=row[1],
                text=row[2],
                author=row[3],
                pub_date=row[4]
                )