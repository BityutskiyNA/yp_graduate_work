import logging

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from redis import Redis
from src.core.config import config
from src.dataclasses.etl.transform import (
    TransformActor,
    TransformDirector,
    TransformFilmwork,
    TransformGenre,
    TransformWriter,
)
from src.helpers.load import _gendata_filmwork, _gendata_others, _put_to_cache


def load(
    logger: logging.Logger,
    cache: Redis,
    es: Elasticsearch,
    data: tuple[
        list[TransformFilmwork],
        list[TransformGenre],
        list[TransformActor],
        list[TransformWriter],
        list[TransformDirector],
    ],
) -> None:
    L_filmwork, L_genre, L_actor, L_writer, L_director = data
    logger.info("Load: filmwork")
    bulk(es, _gendata_filmwork(logger, es, L_filmwork, config.es.filmwork_index))
    logger.info("Load: genre")
    bulk(es, _gendata_others(logger, es, L_genre, config.es.genre_index))
    logger.info("Load: actor")
    bulk(es, _gendata_others(logger, es, L_actor, config.es.actor_index))
    logger.info("Load: writer")
    bulk(es, _gendata_others(logger, es, L_writer, config.es.writer_index))
    logger.info("Load: director")
    bulk(es, _gendata_others(logger, es, L_director, config.es.director_index))
    logger.info("Load: update cache")
    _put_to_cache(logger, cache, L_filmwork)
