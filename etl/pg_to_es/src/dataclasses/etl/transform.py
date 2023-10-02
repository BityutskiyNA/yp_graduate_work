from src.dataclasses.db import Filmwork, Genre, Person


class TransformFilmwork(Filmwork):
    genres: list[Genre]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]
    genres__name: list[str]
    actors__full_name: list[str]
    writers__full_name: list[str]
    directors__full_name: list[str]


class TransformGenre(Genre):
    filmworks__id: list[str]


class TransformActor(Person):
    filmworks__id: list[str]


class TransformWriter(Person):
    filmworks__id: list[str]


class TransformDirector(Person):
    filmworks__id: list[str]
