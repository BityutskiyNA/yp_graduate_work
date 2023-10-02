from http import HTTPStatus
from typing import Optional

from api.v1.schemas import PaginatedPage
from pydantic import BaseModel
from services.film import (
    FilmsAllService,
    FilmService,
    SearchFilmService,
    get_all_films_service,
    get_film_service,
    search_film_service,
)

from fastapi import APIRouter, Depends, HTTPException, Query

FILM_SORT_LIST = ["imdb_rating"]

router = APIRouter()


class Film(BaseModel):
    id: str
    imdb_rating: Optional[float]
    title: str
    genres__name: list[str]
    description: Optional[str] = None
    directors__full_name: Optional[list]
    actors__full_name: Optional[list]
    writers__full_name: Optional[list]
    genres: Optional[list]


class SearchFilm(BaseModel):
    uuid: str
    title: str
    imdb_rating: Optional[float]


@router.get("/search", response_model=PaginatedPage, name="Поиск фильмов")
async def search_film(
    query: str,
    page_number: int = Query(ge=0, default=0, title="Page Number"),
    page_size: int = Query(ge=0, default=10, title="Page Size"),
    film_service: SearchFilmService = Depends(search_film_service),
) -> PaginatedPage:
    films = await film_service.get_data(query, page_number, page_size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film not found")

    total_pages = films.get("total") / page_size + 1

    return PaginatedPage(
        items=[
            SearchFilm(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating)
            for film in films.get("films")
        ],
        first=0,
        last=total_pages - 1,
        prev=page_number - 1 if page_number - 1 >= 0 else None,
        next=page_number + 1 if page_number + 1 <= total_pages - 1 else None,
    )


@router.get("/{film_id}", response_model=Film, name="Детали фильма")
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_data(prefix="film_", id=film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Film not found")

    return Film(**film.dict())


@router.get("/", response_model=PaginatedPage, name="Список фильмов")
async def list_films(
    page_number: int = Query(ge=0, default=0, title="Page Number"),
    page_size: int = Query(ge=0, default=10, title="Page Size"),
    sort="-imdb_rating",
    film_service: FilmsAllService = Depends(get_all_films_service),
) -> PaginatedPage:
    sort_parts = sort.split("-")
    if len(sort_parts) == 2:
        sort = sort_parts[1]
        sort_order = "desc"
    elif len(sort_parts) == 1:
        sort_order = "asc"
    else:
        sort_order = "asc"

    if sort not in FILM_SORT_LIST:
        sort = None
        sort_order = None

    all_films = await film_service.get_data(
        page=page_number, size=page_size, sort=sort, sort_order=sort_order
    )
    if not all_films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Films not found")

    total_pages = all_films.get("total") / page_size + 1

    return PaginatedPage(
        items=[
            SearchFilm(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating)
            for film in all_films.get("films")
        ],
        first=0,
        last=total_pages - 1,
        prev=page_number - 1 if page_number - 1 >= 0 else None,
        next=page_number + 1 if page_number + 1 <= total_pages - 1 else None,
    )
