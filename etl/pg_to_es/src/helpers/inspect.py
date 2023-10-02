import logging
from uuid import uuid4

import pandas as pd
from src.core.config import config


def inspect_ids(logger: logging.Logger, db_cursor, cache) -> tuple[uuid4]:
    ids = []
    counter = 0
    db_cursor.execute(
        f"""SELECT MAX(updated_at) as max_updated_at FROM {config.db.schema_name}.filmwork"""
    )
    max_updated_at = db_cursor.fetchall()[0]["max_updated_at"]
    db_cursor.execute(f"""SELECT * FROM {config.db.schema_name}.filmwork""")
    for row in db_cursor:
        id = str(row["id"])
        updated_at = cache.get(id)
        logger.info(f"Inspect: id={id}, updated_at:{updated_at}")
        if updated_at is None:
            ids.append(id)
            counter += 1
        else:
            cache_updated_at = pd.to_datetime(updated_at.decode("utf-8"), utc=True)
            if cache_updated_at < max_updated_at:
                ids.append(id)
                counter += 1
        if counter >= 10000:
            break
    ids = tuple(ids)
    return ids
