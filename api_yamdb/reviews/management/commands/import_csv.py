import codecs
import csv
import os
from itertools import islice

from django.core.management.base import BaseCommand  # , CommandError

from users.models import User
from reviews.models import Comment, Title, Review
from title.models import Categorie, Genre, GenreTitle


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
                encoding='utf-8',
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
            # Импорт category.csv
            with open(
                'static/data/category.csv',
                'r',
                newline=''
            ) as f:
                reader = csv.reader(f)
                for row in islice(reader, 1, None):
                    _, created = Categorie.objects.get_or_create(
                        id=row[0],
                        name=row[1],
                        slug=row[2]
                    )
            self.stdout.write(
                self.style.SUCCESS(u'Импорт catefory.csv завершён!'))
            # Импорт genre.csv
            with open(
                'static/data/genre.csv',
                'r',
                newline=''
            ) as f:
                reader = csv.reader(f)
                for row in islice(reader, 1, None):
                    _, created = Genre.objects.get_or_create(
                        id=row[0],
                        name=row[1],
                        slug=row[2]
                    )
            self.stdout.write(
                self.style.SUCCESS(u'Импорт genre.csv завершён!'))
            # Импорт titles.csv
            with open(
                'static/data/titles.csv',
                'r',
                newline=''
            ) as f:
                reader = csv.reader(f)
                for row in islice(reader, 1, None):
                    _, created = Title.objects.get_or_create(
                        id=row[0],
                        name=row[1],
                        year=row[2],
                        category_id=row[3]
                    )
            self.stdout.write(
                self.style.SUCCESS(u'Импорт titles.csv завершён!'))
            # Импорт review.csv
            with open(
                'static/data/review.csv',
                'r',
                newline=''
            ) as f:
                reader = csv.reader(f)
                for row in islice(reader, 1, None):
                    _, created = Review.objects.get_or_create(
                        id=row[0],
                        title_id=row[1],
                        text=row[2],
                        author_id=row[3],
                        score=row[4],
                        pub_date=row[5]
                    )
            self.stdout.write(
                self.style.SUCCESS(u'Импорт review.csv завершён!'))
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
                        review_id=row[1],
                        text=row[2],
                        author_id=row[3],
                        pub_date=row[4]
                    )
            self.stdout.write(
                self.style.SUCCESS(u'Импорт comments.csv завершён!'))
            # Импорт genre_title.csv
            with open(
                'static/data/genre_title.csv',
                'r',
                newline=''
            ) as f:
                reader = csv.reader(f)
                for row in islice(reader, 1, None):
                    _, created = GenreTitle.objects.get_or_create(
                        id=row[0],
                        title_id=row[1],
                        genre_id=row[2]
                    )
            self.stdout.write(
                self.style.SUCCESS(u'Импорт genre_title.csv завершён!'))
            self.stdout.write(
                self.style.SUCCESS(u'Операция завершена'))

        except Exception as error:
            self.stdout.write(self.style.WARNING(error))
