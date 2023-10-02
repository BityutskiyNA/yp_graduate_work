from http import HTTPStatus

import aiohttp
import pytest
from tests.functional.settings import test_settings
from tests.functional.testdata import es_data

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def es_write_data_for_genre_api(es_write_data):
    await es_write_data(es_data.es_data_for_tests_genre, "genres")


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        ({"search": "comedy"}, {"status": HTTPStatus.OK, "length": 1}),
        ({"search": "Mashed potato"}, {"status": HTTPStatus.OK, "length": 0}),
    ],
)
async def test_genre_search(es_write_data_for_genre_api, query_data, expected_answer):
    async with aiohttp.ClientSession(trust_env=True) as session:
        url = f"{test_settings.service_url}/api/v1/genres/search"
        query_data = {"query": "comedy"}
        async with session.get(url, params=query_data, ssl=False) as response:
            body = await response.json()
            headers = response.headers
            status = response.status

        assert status == HTTPStatus.OK


# @pytest.mark.parametrize(
#     "query_data, expected_answer",
#     [
#         ({"search": "comedy"}, {"status": HTTPStatus.OK, "length": 1}),
#         ({"search": "Mashed potato"}, {"status": HTTPStatus.OK, "length": 0}),
#     ],
# )
# async def test_genre_search(query_data, expected_answer):
#     pass
