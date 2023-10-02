import logging
from http import HTTPStatus

import aiohttp
import pytest
from tests.functional.settings import test_settings
from tests.functional.testdata import es_data

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def es_write_data_for_film_api(es_write_data):
    await es_write_data(es_data.es_data_for_tests_film, "movies")


async def test_film_details(es_write_data_for_film_api):
    film_id = es_data.es_data_for_tests_film[0].get("id")

    async with aiohttp.ClientSession(trust_env=True) as session:
        url = f"{test_settings.service_url}/api/v1/films/"
        query_data = {"film_id": film_id}
        async with session.get(url, params=query_data, ssl=False) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
        logging.info(body)

        assert status == HTTPStatus.OK


async def test_film_pages_less_than_zero():
    async with aiohttp.ClientSession(trust_env=True) as session:
        url = f"{test_settings.service_url}/api/v1/films/"
        query_data = {"page_number": -1}
        async with session.get(url, params=query_data, ssl=False) as response:
            body = await response.json()
            status = response.status
        await session.close()
        logging.info(body)

        assert status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert body == {
            "detail": [
                {
                    "ctx": {"limit_value": 0},
                    "loc": ["query", "page_number"],
                    "msg": "ensure this value is greater than or equal to 0",
                    "type": "value_error.number.not_ge",
                }
            ]
        }
