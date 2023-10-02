from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from src.models.filmwork import Filmwork
from src.models.filmwork_genre import FilmworkGenre
from src.models.filmwork_person import FilmworkPerson


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


class FilmworkGenreInline(admin.TabularInline):
    model = FilmworkGenre


class FilmworkPersonInline(admin.TabularInline):
    model = FilmworkPerson


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    # отображение жанров и персона в кинопроизведении
    inlines = (
        FilmworkGenreInline,
        FilmworkPersonInline,
    )
    # Отображение полей в списке
    list_display = (
        "title",
        "description",
        "type",
        "imdb_rating",
        "access_level",
        "creation_date",
        "updated_at",
    )
    # # фильтры
    list_filter = ("type", ("genres__name", custom_titled_filter(_("Genre"))))
    # поиск
    search_fields = ("title", "description", "id", "persons__full_name")
