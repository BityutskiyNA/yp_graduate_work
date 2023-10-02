from .base import BaseClass


class Person(BaseClass):
    full_name: str
    filmworks__id: list[str]


class FilmWithRoles(BaseClass):
    roles: list[str]


class PersonWithFilms(Person):
    filmworks__id: list[str]
