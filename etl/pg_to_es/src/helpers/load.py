import json
import logging
from datetime import datetime

from elasticsearch import Elasticsearch
from redis import Redis
from src.dataclasses.etl.transform import TransformFilmwork


def _gendata_filmwork(
    logger: logging.Logger, es: Elasticsearch, L_data: list[dict], index: str
):
    actions = []
    for row in L_data:
        row = json.loads(row.json())
        if es.exists(index=index, id=row["id"]):
            action = {
                "_index": index,
                "_op_type": "update",
                "_type": "_doc",
                "_id": row["id"],
                "_source": row,
            }
        else:
            action = {
                "_index": index,
                "_op_type": "index",
                "_type": "_doc",
                "_id": row["id"],
                "_source": row,
            }
        actions.append(action)
        logger.info(f"\action:{action}")
    return actions


def _gendata_others(
    logger: logging.Logger, es: Elasticsearch, L_data: list[dict], index: str
):
    actions = []
    for row in L_data:
        row = json.loads(row.json())
        if es.exists(index=index, id=row["id"]):
            action = {
                "_index": index,
                "_op_type": "update",
                "_type": "_doc",
                "_id": row["id"],
                "upsert": {"DataIds": row["filmworks__id"]},
                "script": {
                    "source": "ctx._source.DataIds.add(params.DataIds)",
                    "lang": "painless",
                    "params": {"DataIds": row["filmworks__id"]},
                },
            }
        else:
            action = {
                "_index": index,
                "_op_type": "index",
                "_type": "_doc",
                "_id": row["id"],
                "_source": row,
            }
        actions.append(action)
        logger.info(f"\action:{action}")
    return actions


def _put_to_cache(
    logger: logging.Logger, cache: Redis, L_filmwork: list[TransformFilmwork]
) -> None:
    pipeline = cache.pipeline()
    for row in L_filmwork:
        row = json.loads(row.json())
        logger.info(f"\trow:{row}")
        id = str(row["id"])
        updated_at = datetime.now().isoformat()
        pipeline.set(id, updated_at)
    pipeline.execute()
