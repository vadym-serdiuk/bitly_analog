import random
import string

from django.conf import settings
from django.db import models


CHARS = string.ascii_letters + string.digits


class Link(models.Model):
    original_link = models.URLField(unique=True, verbose_name='Original link')
    short_key = models.CharField(max_length=10, unique=True, verbose_name='Short key')
    views_number = models.PositiveIntegerField(default=0, verbose_name='Views number')

    @staticmethod
    def generate_short_link():
        return ''.join([random.choice(CHARS) for _ in range(settings.SHORT_KEY_LENGTH)])

    def save(self, *args, **kwargs):
        # Generate short link while creating a record
        if not self.short_key:
            self.short_key = self.generate_short_link()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.original_link

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'
