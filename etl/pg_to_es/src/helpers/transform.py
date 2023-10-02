import logging

import numpy as np
import pandas as pd
from src.dataclasses.etl.transform import (
    TransformActor,
    TransformDirector,
    TransformFilmwork,
    TransformGenre,
    TransformWriter,
)

ROLES = ["actor", "writer", "director"]


def _transform_filmwork(
    logger: logging.Logger,
    df_f: pd.DataFrame,
    df_fwg: pd.DataFrame,
    df_fwp: pd.DataFrame,
) -> list[TransformFilmwork]:
    df_f = df_f.replace({np.nan: None})
    df_fwg = df_fwg.replace({np.nan: None})
    df_fwp = df_fwp.replace({np.nan: None})

    L_filmwork = []
    for id, subdf in df_f.groupby("id"):
        d = (
            subdf[
                [
                    "id",
                    "title",
                    "description",
                    "creation_date",
                    "imdb_rating",
                    "file_path",
                    "type",
                    "access_level",
                    "updated_at",
                ]
            ]
            .iloc[0]
            .to_dict()
        )
        subdf_genre = df_fwg.query("id==@id")
        d["genres__name"] = subdf_genre["genre_name"].unique().tolist()
        d["genres"] = (
            subdf_genre[["genre_id", "genre_name", "genre_description"]]
            .rename(
                columns={
                    "genre_id": "id",
                    "genre_name": "name",
                    "genre_description": "description",
                }
            )
            .drop_duplicates()
            .to_dict("records")
        )
        subdf_person = df_fwp.query("id==@id")
        for role in ROLES:
            subdf_role = subdf_person.query("person_role==@role")
            d[f"{role}s__full_name"] = subdf_role["person_full_name"].unique().tolist()
            d[f"{role}s"] = (
                subdf_role[["person_id", "person_full_name"]]
                .rename(columns={"person_id": "id", "person_full_name": "full_name"})
                .drop_duplicates()
                .to_dict("records")
            )
        L_filmwork.append(TransformFilmwork(**d))
        logger.info(f"\tfilmwork: {d}")
    return L_filmwork


def _transform_genre(
    logger: logging.Logger, df_fwg: pd.DataFrame
) -> list[TransformGenre]:
    L_genre = []
    for id, subdf in df_fwg.groupby("genre_id"):
        d = (
            subdf[["genre_id", "genre_name", "genre_description"]]
            .rename(
                columns={
                    "genre_id": "id",
                    "genre_name": "name",
                    "genre_description": "description",
                }
            )
            .iloc[0]
            .to_dict()
        )
        d["filmworks__id"] = subdf["id"].values.tolist()
        L_genre.append(TransformGenre(**d))
        logger.info(f"\tgenre:{d}")
    return L_genre


def _transform_person(
    logger: logging.Logger,
    df_fwp: pd.DataFrame,
) -> tuple[list[TransformActor], list[TransformWriter], list[TransformDirector]]:
    L_actor, L_writer, L_director = [], [], []
    for id, subdf in df_fwp.groupby("person_id"):
        for l, role, model in zip(
            (L_actor, L_writer, L_director),
            ROLES,
            [TransformActor, TransformWriter, TransformDirector],
        ):
            subdf_role = subdf.query("person_role==@role")
            if len(subdf_role) != 0:
                d = (
                    subdf_role[["person_id", "person_full_name"]]
                    .rename(
                        columns={"person_id": "id", "person_full_name": "full_name"}
                    )
                    .iloc[0]
                    .to_dict()
                )
                d["filmworks__id"] = subdf_role["id"].values.tolist()
                l.append(model(**d))
                logger.info(f"\t{role}:{d}")
    return L_actor, L_writer, L_director
