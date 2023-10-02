from django.db import models
from django.utils.translation import gettext_lazy as _
from src.core.config import config
from src.models.mixins.datetime import DateTimeMixin
from src.models.mixins.uuid import UUIDMixin


class Person(UUIDMixin, DateTimeMixin):
    """Класс для описания персоны."""

    full_name = models.CharField(max_length=255, verbose_name=_("Full name"))

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = f'{config.db.schema_name}"."person'
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
