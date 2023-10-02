from src.dataclasses.db import Filmwork, Genre, Person


class FilmworkIndex(Filmwork):
    genres__name: list[str]
    actors__full_name: list[str]
    writers__full_name: list[str]
    directors__full_name: list[str]
    genres: list[Genre]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]
