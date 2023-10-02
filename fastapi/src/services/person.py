import logging
import uuid as uuid
from functools import lru_cache
from typing import Optional

from db.elastic import ElasticGetDataMixin, get_elastic_data
from db.redis import RedisManageData, get_redis_data
from models.film import Film
from models.person import FilmWithRoles, Person, PersonWithFilms
from pydantic import BaseModel
from services.base_service import BaseCacheService, BaseService

from fastapi import Depends

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class PersonsFilmDetailed(BaseModel):
    uuid: uuid.UUID
    title: str
    imdb_rating: float


class PersonService(BaseCacheService):
    async def _get_from_search_engine(
        self, person_id: str
    ) -> Optional[PersonWithFilms]:
        doc = await self.search_engine.get_data(schema="actor", id=person_id)
        if not doc:
            doc = await self.search_engine.get_data(schema="director", id=person_id)
        if not doc:
            doc = await self.search_engine.get_data(schema="writer", id=person_id)
        if not doc:
            return None

        person = Person(**doc)
        # films = await GetFilmForPersonService(self.redis, self.search_engine).get_data(person)

        return PersonWithFilms(
            id=person.id,
            full_name=person.full_name,
            filmworks__id=person.filmworks__id,
        )

    async def _get_from_redis(self, composite_id: str) -> Optional[PersonWithFilms]:
        data = await self.redis.get_data(composite_id)
        if not data:
            return None

        person = PersonWithFilms.parse_raw(data)
        return person

    async def _put_to_redis(self, composite_id, person: PersonWithFilms):
        await self.redis.set_data(
            key=composite_id, value=person.json(), expires=FILM_CACHE_EXPIRE_IN_SECONDS
        )

    async def get_data(self, *args, **kwargs) -> Optional[PersonWithFilms]:
        return await super().get_data(*args, **kwargs)


class GetFilmForPersonService(BaseService):
    async def _get_from_search_engine(
        self, person: Person
    ) -> Optional[list[FilmWithRoles]]:
        film_docs = await self.search_engine.get_data(
            schema="filmwork", ids=person.filmworks__id
        )
        if not film_docs:
            return []

        films: list[FilmWithRoles] = []
        for film in film_docs:
            film_data = film["_source"]
            roles = []
            if person.id in [person.get("id") for person in film_data.get("writers")]:
                roles.append("writer")

            if person.id in [person.get("id") for person in film_data.get("actors")]:
                roles.append("actor")

            if person.id in [person.get("id") for person in film_data.get("directors")]:
                roles.append("director")

            films.append(
                FilmWithRoles(
                    id=film_data.get("id"),
                    roles=roles,
                )
            )
        return films


class PersonFilmsService(BaseCacheService):
    async def _get_from_search_engine(
        self, person_id: str
    ) -> Optional[list[PersonsFilmDetailed]]:
        doc = await self.search_engine.get_data(schema="actor", id=person_id)
        if not doc:
            doc = await self.search_engine.get_data(schema="director", id=person_id)
        if not doc:
            doc = await self.search_engine.get_data(schema="writer", id=person_id)
        if not doc:
            return None

        person = Person(**doc)

        film_doc = await self.search_engine.get_data(
            schema="filmwork", ids=person.filmworks__id
        )
        if not film_doc:
            return []

        films: list[PersonsFilmDetailed] = []

        for film in film_doc:
            film_data = Film(**film["_source"])
            films.append(
                PersonsFilmDetailed(
                    uuid=film_data.id,
                    title=film_data.title,
                    imdb_rating=film_data.imdb_rating,
                )
            )
        return films

    async def _get_from_redis(
        self, composite_id: str
    ) -> Optional[list[PersonsFilmDetailed]]:
        data = await self.redis.get_dataset(composite_id)
        logging.info("Data found in Redis")
        if not data:
            return None

        films: list[PersonsFilmDetailed] = []
        for raw_film in data:
            films.append(PersonsFilmDetailed.parse_raw(raw_film))
        return films

    async def _put_to_redis(
        self, composite_id: str, person_films: list[PersonsFilmDetailed]
    ):
        await self.redis.delete_and_push_list(
            composite_id=composite_id, data_list=person_films, match="person_*"
        )


class SearchPersonService(BaseService):
    async def _get_from_search_engine(
        self, query: str, page_number: int, page_size: int
    ) -> Optional[dict[Optional[str], Optional[PersonWithFilms]]]:
        docs = await self.search_engine.get_data(
            index="actor",
            query=query,
            param_name="full_name",
            page_size=page_size,
            page_number=page_number,
        )
        if not docs:
            docs = await self.search_engine.get_data(
                index="writer",
                query=query,
                param_name="full_name",
                page_size=page_size,
                page_number=page_number,
            )
        if not docs:
            docs = await self.search_engine.get_data(
                index="director",
                query=query,
                param_name="full_name",
                page_size=page_size,
                page_number=page_number,
            )
        if not docs:
            return None

        persons = []
        for line in docs.get("hits"):
            person = Person(**line["_source"])
            # films = await GetFilmForPersonService(self.redis, self.search_engine).get_data(
            #     person
            # )
            persons.append(
                PersonWithFilms(
                    id=person.id,
                    full_name=person.full_name,
                    filmworks__id=person.filmworks__id,
                )
            )
        if docs.get("total") and docs["total"].get("value"):
            total_docs = docs["total"]["value"]
        else:
            total_docs = 0
        return {
            "total": total_docs,
            "persons": persons,
        }


@lru_cache()
def get_person_service(
    redis: RedisManageData = Depends(get_redis_data),
    search_engine: ElasticGetDataMixin = Depends(get_elastic_data),
) -> PersonService:
    return PersonService(redis, search_engine)


@lru_cache()
def get_person_films_service(
    redis: RedisManageData = Depends(get_redis_data),
    search_engine: ElasticGetDataMixin = Depends(get_elastic_data),
) -> PersonFilmsService:
    return PersonFilmsService(redis, search_engine)


@lru_cache()
def search_person_service(
    redis: RedisManageData = Depends(get_redis_data),
    search_engine: ElasticGetDataMixin = Depends(get_elastic_data),
) -> SearchPersonService:
    return SearchPersonService(redis, search_engine)
