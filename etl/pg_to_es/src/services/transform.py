import json
import logging

import numpy as np
import pandas as pd
from src.dataclasses.etl.extract import (
    ExtractFilmwork,
    ExtractFilmworkGenre,
    ExtractFilmworkPerson,
)
from src.dataclasses.etl.transform import (
    TransformActor,
    TransformDirector,
    TransformFilmwork,
    TransformGenre,
    TransformWriter,
)
from src.helpers.transform import (
    _transform_filmwork,
    _transform_genre,
    _transform_person,
)


def transform(
    logger: logging.Logger,
    data: dict[
        list[ExtractFilmwork], list[ExtractFilmworkGenre], list[ExtractFilmworkPerson]
    ],
) -> tuple[
    list[TransformFilmwork],
    list[TransformGenre],
    list[TransformActor],
    list[TransformWriter],
    list[TransformDirector],
]:
    df_f = pd.DataFrame.from_records(
        [json.loads(row.json()) for row in data["filmwork"]]
    )
    df_fwg = pd.DataFrame.from_records(
        [json.loads(row.json()) for row in data["filmwork_genre"]]
    )
    df_fwp = pd.DataFrame.from_records(
        [json.loads(row.json()) for row in data["filmwork_person"]]
    )

    logger.info("Transform: filmwork data")
    L_filmwork = _transform_filmwork(logger, df_f, df_fwg, df_fwp)
    logger.info("Transform: filmwork genre")
    L_genre = _transform_genre(logger, df_fwg)
    logger.info("Transform: filmwork person")
    L_actor, L_writer, L_director = _transform_person(logger, df_fwp)
    return L_filmwork, L_genre, L_actor, L_writer, L_director
