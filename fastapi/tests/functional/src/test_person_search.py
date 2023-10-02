from http import HTTPStatus

import pytest
from tests.functional.testdata.es_data import (
    Persons,
    es_data_films_for_persons,
    es_data_person_by_id_index,
)

pytestmark = pytest.mark.asyncio


PAGE_SIZE = 10


class TestPersonSearch:
    search_url = "/api/v1/persons/search"
    number = 100

    async def es_write_data_for_persons(self, es_write_data, number=None):
        if not number:
            number = self.number
        persons = Persons(number)
        persons.get_es_data_persons()
        persons.get_es_data_persons_films()
        await es_write_data(persons.persons, "persons")
        await es_write_data(persons.films, "movies")

    async def test_get_person_search_without_params(
        self,
        make_get_request,
        es_write_data,
    ):
        await self.es_write_data_for_persons(es_write_data)

        response = await make_get_request(self.search_url)
        body = await response.json()

        assert response.status == HTTPStatus.OK
        assert body.get("first") == 0
        assert body.get("last") == self.number / PAGE_SIZE
        assert body.get("next") == 1
        assert body.get("prev") is None
        assert len(body.get("items")) == PAGE_SIZE

    @pytest.mark.parametrize(
        "number,page_number,page_size,next,prev,items",
        [
            (100, 0, 10, 1, None, 10),
            (100, 1, 10, 2, 0, 10),
            (100, 9, 10, 10, 8, 10),
            (99, 0, 100, None, None, 99),
        ],
    )
    async def test_get_person_search_page_params(
        self,
        make_get_request,
        es_write_data,
        number,
        page_number,
        page_size,
        next,
        prev,
        items,
    ):
        await self.es_write_data_for_persons(es_write_data, number)

        query_data = {"page_number": page_number, "page_size": page_size}
        response = await make_get_request(self.search_url, query_data)
        body = await response.json()

        assert response.status == HTTPStatus.OK
        assert body.get("first") == 0
        assert body.get("last") == number // page_size
        assert body.get("next") == next
        assert body.get("prev") == prev
        assert len(body.get("items")) == items

    async def test_get_person_search_not_found(
        self,
        make_get_request,
        es_write_data,
    ):
        await self.es_write_data_for_persons(es_write_data)

        query_data = {"query": "TestTestTest"}
        response = await make_get_request(self.search_url, query_data=query_data)
        body = await response.json()

        assert response.status == HTTPStatus.OK
        assert body == {"first": 0, "items": [], "last": 0, "next": None, "prev": None}

    async def test_get_person_search_find(
        self,
        make_get_request,
        person_id,
        es_write_data,
        persons_expected_answer: dict,
    ):
        await es_write_data(es_data_person_by_id_index, "persons")
        await es_write_data(es_data_films_for_persons, "movies")

        query_data = {"query": "Ann"}
        response = await make_get_request(self.search_url, query_data=query_data)
        assert response.status == HTTPStatus.OK

        body = await response.json()
        assert body == {
            "first": 0,
            "items": [persons_expected_answer],
            "last": 0,
            "next": None,
            "prev": None,
        }

    @pytest.mark.parametrize("query_name", ["page_number", "page_size"])
    async def test_get_person_search_incorrect_number(
        self,
        make_get_request,
        es_write_data,
        query_name,
    ):
        await es_write_data(es_data_person_by_id_index, "persons")
        await es_write_data(es_data_films_for_persons, "movies")

        query_data = {"query": "Ann", query_name: -1}
        response = await make_get_request(self.search_url, query_data=query_data)

        assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY

    async def test_get_person_search_correct_number(
        self,
        make_get_request,
        es_write_data,
    ):
        await es_write_data(es_data_person_by_id_index, "persons")
        await es_write_data(es_data_films_for_persons, "movies")

        query_data = {"query": "Ann", "page_number": 0, "page_size": 1}
        response = await make_get_request(self.search_url, query_data=query_data)

        assert response.status == HTTPStatus.OK
