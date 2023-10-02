from django.db import models
from django.utils.translation import gettext_lazy as _
from src.core.config import config
from src.models.mixins.uuid import UUIDMixin


class FilmworkGenre(UUIDMixin):
    """Класс для описания жанров кинопроизведения."""

    filmwork = models.ForeignKey(
        to="Filmwork",
        db_column="filmwork_id",
        on_delete=models.CASCADE,
        verbose_name=_("Filmwork"),
    )
    genre = models.ForeignKey(
        to="Genre",
        db_column="genre_id",
        on_delete=models.CASCADE,
        verbose_name=_("Genre"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    def __str__(self):
        return "Жанры кинопроизведения"

    class Meta:
        db_table = f'{config.db.schema_name}"."filmwork_genre'
        verbose_name = _("FilmworkGenre")
        verbose_name_plural = _("FilmworkGenres")
