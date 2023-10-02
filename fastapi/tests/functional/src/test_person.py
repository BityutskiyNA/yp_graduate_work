from http import HTTPStatus

import pytest
from tests.functional.testdata.es_data import (
    es_data_films_for_persons,
    es_data_person_by_id_index,
)

pytestmark = pytest.mark.asyncio


@pytest.fixture
def person_id_not_found():
    return "22222"


@pytest.fixture
async def expected_answer_film():
    return [
        {
            "imdb_rating": 8.5,
            "title": "The Star",
            "uuid": "e95044a7-1f66-4164-9650-3bf2132d7119",
        },
        {
            "imdb_rating": 8.5,
            "title": "The Star",
            "uuid": "5f1a4219-b533-489f-8af2-0d2692504857",
        },
    ]


@pytest.fixture
async def es_write_data_for_person_api(es_write_data):
    await es_write_data(es_data_person_by_id_index, "persons")
    await es_write_data(es_data_films_for_persons, "movies")


class TestPersonById:
    async def test_get_person(
        self,
        make_get_request,
        es_write_data_for_person_api,
        person_id,
        persons_expected_answer: dict,
    ):
        response = await make_get_request(f"/api/v1/persons/{person_id}")
        body = await response.json()

        assert response.status == HTTPStatus.OK
        assert body == persons_expected_answer

    async def test_get_person_error(
        self,
        make_get_request,
        person_id_not_found,
    ):
        response = await make_get_request(f"/api/v1/persons/{person_id_not_found}")
        body = await response.json()

        assert response.status == HTTPStatus.NOT_FOUND
        assert body == {"detail": "person not found"}

    async def test_get_person_film_error(
        self,
        make_get_request,
        person_id_not_found,
    ):
        response = await make_get_request(f"/api/v1/persons/{person_id_not_found}/film")
        body = await response.json()

        assert response.status == HTTPStatus.NOT_FOUND
        assert body == {"detail": "person not found"}

    async def test_get_person_film(
        self,
        make_get_request,
        es_write_data_for_person_api,
        person_id,
        expected_answer_film: list,
    ):
        response = await make_get_request(f"/api/v1/persons/{person_id}/film")
        body = await response.json()

        assert response.status == HTTPStatus.OK
        assert len(body) == len(expected_answer_film)
        assert set(body) == set(expected_answer_film)
