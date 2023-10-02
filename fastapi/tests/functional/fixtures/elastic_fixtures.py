from typing import List

import pytest
from elasticsearch import AsyncElasticsearch
from tests.functional.conftest import get_es_bulk_query
from tests.functional.settings import TestSettings


def get_settings() -> TestSettings:
    return TestSettings()


test_settings = get_settings()


@pytest.fixture
async def es_client():
    client = AsyncElasticsearch(
        hosts=test_settings.elastic_host, validate_cert=False, use_ssl=False
    )
    yield client
    await client.indices.flush()
    await client.close()


@pytest.fixture
def es_write_data(es_client):
    async def inner(data: List[dict], index: str):
        print(es_client)
        bulk_query = get_es_bulk_query(data, index)
        str_query = "\n".join(bulk_query) + "\n"

        index_exists = await es_client.indices.exists(index=index)
        if index_exists:
            await es_client.indices.delete(index=index)

        response = await es_client.bulk(str_query, refresh=True)
        if response["errors"]:
            raise Exception("Ошибка записи данных в Elasticsearch")
        return response

    return inner
