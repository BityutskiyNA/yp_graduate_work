import json
from typing import List

import aiohttp
import pytest
from tests.functional.settings import TestSettings


def get_settings() -> TestSettings:
    return TestSettings()


test_settings = get_settings()

pytest_plugins = "tests.functional.fixtures"


def get_es_bulk_query(data: List[dict], index: str):
    bulk_query = []
    for row in data:
        bulk_query.extend(
            [
                json.dumps(
                    {"index": {"_index": index, "_id": row[test_settings.es_id_field]}}
                ),
                json.dumps(row),
            ]
        )
    return bulk_query


@pytest.fixture
def make_get_request():
    async def inner(url_ending, query_data=None):
        async with aiohttp.ClientSession(trust_env=True) as session:
            url = test_settings.service_url + url_ending
            return await session.get(url, params=query_data, ssl=False)

    return inner
