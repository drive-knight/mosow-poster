from pathlib import Path
from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название места')
    slug = models.SlugField(unique=True)
    description_short = models.TextField(blank=True, verbose_name='Короткое описание')
    description_long = HTMLField(blank=True, verbose_name='Описание')
    lng = models.FloatField(null=True, blank=True, verbose_name='Широта')
    lat = models.FloatField(null=True, blank=True, verbose_name='Долгота')

    class Meta:
        ordering = ('title',)
        unique_together = ['lng', 'lat']

    def __str__(self):
        return self.title


def get_upload_path(instance, filename):
    return Path(instance.place.slug) / filename


class Image(models.Model):
    place = models.ForeignKey(to=Place, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_upload_path, verbose_name='Изображение')
    index = models.PositiveIntegerField(db_index=True, default=1, blank=True)

    class Meta:
        ordering = ('index',)
        unique_together = ['place']
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f'{self.pk} {self.place}'