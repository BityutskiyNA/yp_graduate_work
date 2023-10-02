from django.db import models
from django.utils.translation import gettext_lazy as _
from src.core.config import config
from src.models.mixins.datetime import DateTimeMixin
from src.models.mixins.uuid import UUIDMixin


class Genre(UUIDMixin, DateTimeMixin):
    """Класс для описания жанра."""

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(
        verbose_name=_("Description"), blank=True, null=True, default=""
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = f'{config.db.schema_name}"."genre'
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
