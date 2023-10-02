import uuid as uuid
from http import HTTPStatus

from api.v1.schemas import PaginatedPage
from pydantic import BaseModel
from services.person import (
    PersonFilmsService,
    PersonService,
    SearchPersonService,
    get_person_films_service,
    get_person_service,
    search_person_service,
)

from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter()


class PersonsFilm(BaseModel):
    uuid: str
    roles: list[str]


class PersonsFilmDetailed(BaseModel):
    uuid: uuid.UUID
    title: str
    imdb_rating: float


class Person(BaseModel):
    uuid: str
    full_name: str
    filmworks__id: list[str]


@router.get(
    "/search",
    response_model=PaginatedPage,
    summary="Поиск персоны",
    description="Полнотекстовый поиск персоны",
    response_description="Список персон",
)
async def search_person(
    query: str = "",
    page_number: int = Query(ge=0, default=0, title="Page Number"),
    page_size: int = Query(ge=0, default=10, title="Page Size"),
    search_person_service: SearchPersonService = Depends(search_person_service),
) -> PaginatedPage:
    data = await search_person_service.get_data(query, page_number, page_size)
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")

    persons = data["persons"]
    total_pages = data.get("total") / page_size + 1

    # if page_number > total_pages or page_number < 0:
    #     raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='wrong page number')

    return PaginatedPage(
        items=[
            Person(
                uuid=person.id,
                full_name=person.full_name,
                filmworks__id=person.filmworks__id,
            )
            for person in persons
        ],
        first=0,
        last=total_pages - 1,
        prev=page_number - 1 if page_number - 1 >= 0 else None,
        next=page_number + 1 if page_number + 1 <= total_pages - 1 else None,
    )


@router.get(
    "/{person_id}",
    response_model=Person,
    summary="Получение персоны",
    description="Получение данных персоны по id",
    response_description="Имя персоны и фильмы, в которых он участвовал с ролями",
)
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> Person:
    person = await person_service.get_data(prefix="person_", id=person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")

    return Person(
        uuid=person.id,
        full_name=person.full_name,
        filmworks__id=person.filmworks__id,
    )


@router.get(
    "/{person_id}/film",
    response_model=list[PersonsFilmDetailed],
    summary="Фильмы персоны",
    description="Получение данных фильмов по персоне",
    response_description="Название и рейтинг фильма",
)
async def person_films(
    person_id: str,
    person_service: PersonFilmsService = Depends(get_person_films_service),
) -> list[PersonsFilmDetailed]:
    films = await person_service.get_data("person_films", person_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")

    return [PersonsFilmDetailed(**film.dict()) for film in films]
