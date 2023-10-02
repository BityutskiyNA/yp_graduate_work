import json
import logging
from uuid import UUID

from psycopg2.extensions import cursor
from src.dataclasses.etl.extract import (
    ExtractFilmwork,
    ExtractFilmworkGenre,
    ExtractFilmworkPerson,
)
from src.helpers.extract import (
    __extract__filmwork,
    __extract__filmwork_genre,
    __extract__filmwork_person,
)


def extract(
    logger: logging.Logger, db_cursor: cursor, ids: list[UUID]
) -> dict[
    list[ExtractFilmwork], list[ExtractFilmworkGenre], list[ExtractFilmworkPerson]
]:
    logger.info("Extract: filmwork data ...")
    filmwork_data = [
        ExtractFilmwork(**row) for row in __extract__filmwork(db_cursor, ids)
    ]
    logger.info("Extract: filmwork_genre data ...")
    filmwork_genre_data = [
        ExtractFilmworkGenre(**row) for row in __extract__filmwork_genre(db_cursor, ids)
    ]
    logger.info("Extract: filmwork_person data ...")
    filmwork_person_data = [
        ExtractFilmworkPerson(**row)
        for row in __extract__filmwork_person(db_cursor, ids)
    ]
    data = {
        "filmwork": filmwork_data,
        "filmwork_genre": filmwork_genre_data,
        "filmwork_person": filmwork_person_data,
    }
    return data
