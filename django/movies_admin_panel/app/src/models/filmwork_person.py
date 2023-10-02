from django.db import models
from django.utils.translation import gettext_lazy as _
from src.core.config import config
from src.models.mixins.uuid import UUIDMixin


class FilmworkPerson(UUIDMixin):
    """Класс для описания персон кинопроизведения."""

    filmwork = models.ForeignKey(
        to="Filmwork",
        db_column="filmwork_id",
        on_delete=models.CASCADE,
        verbose_name=_("Filmwork"),
    )
    person = models.ForeignKey(
        to="Person",
        db_column="person_id",
        on_delete=models.CASCADE,
        verbose_name=_("Person"),
    )
    role = models.TextField(verbose_name=_("Role"), blank=True, null=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    def __str__(self):
        return "Персоны кинопроизведения"

    class Meta:
        indexes = [
            models.Index(fields=["filmwork", "person", "role"]),
        ]
        db_table = f'{config.db.schema_name}"."filmwork_person'
        verbose_name = _("FilmworkPerson")
        verbose_name_plural = _("FilmworkPersons")
