from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from src.core.config import config
from src.models.mixins.datetime import DateTimeMixin
from src.models.mixins.uuid import UUIDMixin


class Filmwork(UUIDMixin, DateTimeMixin):
    """Класс для описания кинопроизведения."""

    class Type(models.TextChoices):
        """Класс для описания типа кинопроизведения."""

        MOVIE = "movie", _("Movie")
        SERIAL = "serial", _("Serial")
        CARTOON = "cartoon", _("Cartoon")
        TV_SHOW = "tv_show", _("TV show")

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(
        verbose_name=_("Description"), blank=True, null=True, default=""
    )
    creation_date = models.DateField(
        verbose_name=_("Creation date"), blank=True, null=True
    )
    file_path = models.FileField(
        verbose_name=_("Path to file"), blank=True, null=True, default=""
    )
    imdb_rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("IMDB Rating"),
        blank=True,
        null=True,
    )
    type = models.CharField(
        max_length=255,
        choices=Type.choices,
        default=Type.MOVIE,
        verbose_name=_("Type"),
    )
    access_level = models.IntegerField(
        verbose_name=_("Access level"),
        blank=True,
        null=True,
    )

    genres = models.ManyToManyField(
        "Genre", through="FilmworkGenre", verbose_name=_("Genres")
    )
    persons = models.ManyToManyField(
        "Person", through="FilmworkPerson", verbose_name=_("Persons")
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = f'{config.db.schema_name}"."filmwork'
        verbose_name = _("Filmwork")
        verbose_name_plural = _("Filmworks")
