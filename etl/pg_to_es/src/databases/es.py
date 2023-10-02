import json
import logging
from http import HTTPStatus
from pathlib import Path

import backoff
from elasticsearch import ConnectionError, Elasticsearch
from src.core.config import config

BASE_DIR = Path(__file__).resolve().parent.parent


@backoff.on_exception(backoff.expo, ConnectionError, max_tries=config.backoff_max_tries)
def get_es_client(logger: logging.Logger) -> Elasticsearch:
    """Get elasticsearch instance."""
    params = {"host": config.docker.es_host, "port": config.es.port}
    try:
        es_client = Elasticsearch(retry_on_timeout=True, **params)
        _prepare_es_client(
            config.es.filmwork_mapping, config.es.filmwork_index, es_client
        )
        _prepare_es_client(config.es.genre_mapping, config.es.genre_index, es_client)
        _prepare_es_client(config.es.actor_mapping, config.es.actor_index, es_client)
        _prepare_es_client(config.es.writer_mapping, config.es.writer_index, es_client)
        _prepare_es_client(
            config.es.director_mapping, config.es.director_index, es_client
        )
        return es_client
    except ConnectionError as e:
        logger.error(e)


def _prepare_es_client(
    mapping: str, index: str, client: Elasticsearch
) -> Elasticsearch:
    with open(BASE_DIR / "core/mappings" / mapping, "r") as f:
        mapping = json.load(f)
    indices = client.indices.get_alias()
    if index not in indices.keys():
        client.indices.create(index=index, ignore=HTTPStatus.BAD_REQUEST, body=mapping)
    return client
