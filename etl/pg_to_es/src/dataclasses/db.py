from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, FilePath


class IdMixin(BaseModel):
    id: str


class Role(Enum):
    ACTOR = "actor"
    WRITER = "writer"
    DIRECTOR = "director"


class Type(Enum):
    MOVIE = "movie"
    SERIAL = "serial"
    CARTOON = "cartoon"
    TV_SHOW = "tv_show"


class Filmwork(IdMixin):
    title: str
    description: str | None
    creation_date: date | None
    imdb_rating: float | None
    file_path: FilePath | None
    type: Type | None
    access_level: int | None
    updated_at: datetime


class FilmworkGenre(IdMixin):
    genre_id: str
    genre_name: str
    genre_description: str | None


class FilmworkPerson(IdMixin):
    person_id: str
    person_role: Role
    person_full_name: str


class Genre(IdMixin):
    name: str
    description: str | None


class Person(IdMixin):
    full_name: str
