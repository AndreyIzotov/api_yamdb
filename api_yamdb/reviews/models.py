from django.db import models

from reviews.settings import (
    GRADE_CHOICES,
    FACTOR_FOR_REVIEW,
    FACTOR_FOR_COMMENT
)
from reviews.validators import year_title_validate
from users.models import User


class Categorie(models.Model):
    """Категория."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанр."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение."""
    name = models.TextField()
    year = models.PositiveIntegerField(validators=[year_title_validate])
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Categorie, on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name='Категория',
        blank=False, null=True
    )
    genre = models.ManyToManyField(Genre, blank=True, related_name='titles')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['year']

    def __str__(self):
        return f'{self.name} ({self.category})'


class CreatedModel(models.Model):
    """Абстрактная модель.
    Добавляет дату создания."""
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']


class Review(CreatedModel):
    """Модель отзыва."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
        help_text='Произведение, к которому относится отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор',
        help_text='Автор отзыва'
    )
    score = models.IntegerField(default=5, choices=GRADE_CHOICES)
    text = models.TextField('Текст', help_text='Текст нового отзыва')

    class Meta(CreatedModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:FACTOR_FOR_REVIEW]


class Comment(CreatedModel):
    """Модель комментария."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв',
        help_text='Отзыв, к которому относится комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор',
        help_text='Автор комментария'
    )
    text = models.TextField('Текст', help_text='ваш комментарий')

    class Meta(CreatedModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return self.text[:FACTOR_FOR_COMMENT]
