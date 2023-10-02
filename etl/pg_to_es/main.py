import time
import warnings

from src.core.logger import get_logger
from src.databases.cache import get_cache_client
from src.databases.db import get_db_cursor
from src.databases.es import get_es_client
from src.helpers.inspect import inspect_ids
from src.services.extract import extract
from src.services.load import load
from src.services.transform import transform

warnings.filterwarnings("ignore")


def main(iteration: int):
    logger = get_logger(iteration)
    db_cursor = get_db_cursor(logger)
    es = get_es_client(logger)
    cache = get_cache_client(logger)
    count_loaded_records = len(cache.keys())
    logger.info(f'\n\n\nREDIS COUNT "filmwork" ={count_loaded_records}\n\n\n')
    time.sleep(3)

    ids = inspect_ids(logger, db_cursor, cache)
    if len(ids) != 0:
        # try:
        data = extract(logger, db_cursor, ids)
        data_transformed = transform(logger, data)
        load(logger, cache, es, data_transformed)
        # except Exception as e:
        #     logger.error(e)
        #     pass
        # finally:
        #     db_cursor.close()
        #     es.transport.close()
        #     del cache, db_cursor, es


if __name__ == "__main__":
    iteration = 1
    while True:
        main(iteration)
        iteration += 1
