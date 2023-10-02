from uuid import UUID

import pandas as pd
from psycopg2.extensions import cursor
from src.core.config import config


def __extract__filmwork(db_cursor: cursor, ids: tuple[UUID]):
    q = f"""
        SELECT
            id,  title, description, creation_date, imdb_rating, file_path, type, access_level, updated_at
        FROM {config.db.schema_name}.filmwork f WHERE f.id in %(ids)s;
        """
    db_cursor.execute(q, {"ids": ids})
    return db_cursor.fetchall()


def __extract__filmwork_genre(db_cursor: cursor, ids: tuple[UUID]):
    q = f"""
        SELECT
            fwg.filmwork_id as id,
            fwg.genre_id as genre_id,
            g.name as genre_name,
            g.description as genre_description,
            g.updated_at as genre_updated_at
        FROM {config.db.schema_name}.filmwork_genre fwg
            LEFT JOIN {config.db.schema_name}.genre g ON fwg.genre_id = g.id
        WHERE fwg.filmwork_id in %(ids)s;
        """
    db_cursor.execute(q, {"ids": ids})
    return db_cursor.fetchall()


def __extract__filmwork_person(db_cursor: cursor, ids: tuple[UUID]):
    q = f"""
        SELECT
            fwp.filmwork_id as id,
            fwp.person_id as person_id,
            fwp.role as person_role,
            p.full_name as person_full_name,
            p.updated_at as person_updated_at
        FROM {config.db.schema_name}.filmwork_person fwp
            LEFT JOIN {config.db.schema_name}.person p ON fwp.person_id = p.id
        WHERE fwp.filmwork_id in %(ids)s;
        """
    db_cursor.execute(q, {"ids": ids})
    return db_cursor.fetchall()
