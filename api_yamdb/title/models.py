from django.db import models


class Categorie(models.Model):
    """Категория."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанр."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение."""
    name = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Categorie, on_delete=models.SET_NULL,
        related_name="Titles",
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


class GenreTitle(models.Model):
    """Жанры произведений."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre',
        verbose_name='Жанр',
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='title',
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'
