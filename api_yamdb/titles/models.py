from django.db import models

from titles.validators import year_title_validate


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
    genre = models.ManyToManyField(Genre, blank=True, related_name="titles")

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['year']

    def __str__(self):
        return f'{self.name} ({self.category})'
