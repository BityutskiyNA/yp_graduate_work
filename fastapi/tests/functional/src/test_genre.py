import logging

import aiohttp
import pytest
from tests.functional.settings import test_settings
from tests.functional.testdata import es_data

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def es_write_data_for_genre_api(es_write_data):
    await es_write_data(es_data.es_data_for_tests_genre, "genres")


async def test_genre_details(es_write_data_for_genre_api):
    genre_id = es_data.es_data_for_tests_genre[0].get("id")

    async with aiohttp.ClientSession(trust_env=True) as session:
        url = f"{test_settings.service_url}/api/v1/genres/"
        query_data = {"genre_id": genre_id}
        async with session.get(url, params=query_data, ssl=False) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        await session.close()
        logging.info(body)

        assert status == 200
