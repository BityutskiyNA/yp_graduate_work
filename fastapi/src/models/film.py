from typing import Optional

from .base import BaseClass


class Person(BaseClass):
    name: str


class Genre(BaseClass):
    name: str
    description: Optional[str]


class Film(BaseClass):
    imdb_rating: Optional[float]
    title: str
    genres__name: list[str]
    description: Optional[str] = None
    directors__full_name: list[str]
    actors__full_name: list[str]
    writers__full_name: list[str]
    genres: list[Genre]
