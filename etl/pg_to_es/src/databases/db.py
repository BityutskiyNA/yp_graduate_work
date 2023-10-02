import logging

import backoff
import psycopg2
from psycopg2.errors import ConnectionException
from psycopg2.extensions import cursor
from psycopg2.extras import RealDictCursor
from src.core.config import config


@backoff.on_exception(
    backoff.expo, ConnectionException, max_tries=config.backoff_max_tries
)
def get_db_cursor(logger: logging.Logger) -> cursor:
    """Get postgres engine."""
    try:
        conn = psycopg2.connect(
            user=config.db.user,
            password=config.db.password,
            host=config.docker.db_host,
            port=config.db.port,
            dbname=config.db.database,
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        return cur
    except ConnectionException as error:
        logger.error(error)
