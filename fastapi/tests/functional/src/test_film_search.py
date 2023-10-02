from http import HTTPStatus

import aiohttp
import pytest
from tests.functional.settings import test_settings
from tests.functional.testdata import es_data

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def es_write_data_for_film_api(es_write_data):
    await es_write_data(es_data.es_data_for_tests_film, "movies")


async def test_film_search(es_write_data_for_film_api):
    async with aiohttp.ClientSession(trust_env=True) as session:
        url = f"{test_settings.service_url}/api/v1/films/search"
        query_data = {"query": "The Star", "page_number": 1, "page_size": 10}
        async with session.get(url, params=query_data, ssl=False) as response:
            body = await response.json()
            status = response.status

        assert status == HTTPStatus.OK
        assert len(body.get("items")) == 10


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"search": "The Star"}, {"status": HTTPStatus.OK, "length": 10}),
        ({"search": "Mashed potato"}, {"status": HTTPStatus.OK, "length": 0}),
    ],
)
async def test_film_search_1(query_data, expected_answer):
    pass
