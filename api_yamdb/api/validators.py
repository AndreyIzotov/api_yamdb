from django.core.exceptions import ValidationError
import datetime


def year_title_validate(value):
    if datetime.datetime.now().year < value:
        raise ValidationError(f'Дата публикации {value} больше текущего года!')
