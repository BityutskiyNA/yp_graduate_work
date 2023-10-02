import uuid as uuid
from http import HTTPStatus
from typing import Optional

from api.v1.schemas import PaginatedPage
from pydantic import BaseModel
from services.genre import (
    GenreAllService,
    GenreService,
    SearchGenreService,
    get_genre_all_service,
    get_genre_service,
    search_genre_service,
)

from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter()


class Genre(BaseModel):
    uuid: uuid.UUID
    name: str
    description: Optional[str]


@router.get("/search", response_model=Genre, name="Поиск жанров")
async def search_genre(
    query: str, genre_service: SearchGenreService = Depends(search_genre_service)
) -> Genre:
    genre = await genre_service.get_data(query)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre not found")

    return Genre(
        uuid=genre.id,
        name=genre.name,
        description=genre.description,
    )


@router.get("/{genre_id}", response_model=Genre, name="Детали жанра")
async def genre_details(
    genre_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    print(genre_id)
    genre = await genre_service.get_data(prefix="genre_", id=genre_id)
    print(genre)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genre not found")

    return Genre(
        uuid=genre.id,
        name=genre.name,
        description=genre.description,
    )


@router.get("/", name="Список жанров")
async def list_genres(
    page_number: int = Query(ge=0, default=0, title="Page Number"),
    page_size: int = Query(ge=0, default=10, title="Page Size"),
    genre_service: GenreAllService = Depends(get_genre_all_service),
) -> PaginatedPage:
    all_genres = await genre_service.get_data(
        prefix=f"all_genres_{page_number}_{page_size}",
        page=page_number,
        size=page_size,
    )
    if not all_genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Genres not found")
    total_pages = all_genres.get("total") / page_size + 1

    return PaginatedPage(
        items=[
            Genre(
                uuid=genre.get("id"),
                name=genre.get("name"),
                description=genre.get("description"),
            )
            for genre in all_genres.get("genres")
        ],
        first=0,
        last=total_pages - 1,
        prev=page_number - 1 if page_number - 1 >= 0 else None,
        next=page_number + 1 if page_number + 1 <= total_pages - 1 else None,
    )
