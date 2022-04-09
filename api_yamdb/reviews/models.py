from django.db import models

from reviews.settings import (
    GRADE_CHOICES,
    FACTOR_FOR_REVIEW,
    FACTOR_FOR_COMMENT
)
from title.models import Title
from users.models import User


class CreatedModel(models.Model):
    """Абстрактная модель.
    Добавляет дату создания."""
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True


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
