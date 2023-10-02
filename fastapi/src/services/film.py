import logging
from functools import lru_cache
from typing import Any, Optional, Union

from db.elastic import ElasticGetDataMixin, get_elastic_data
from db.redis import RedisManageData, get_redis_data
from models.film import Film
from services.base_service import BaseCacheService, BaseService

from fastapi import Depends

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут
FILMS_PER_PAGE = 10
FILMS_PER_SEARCH = 3


class FilmService(BaseCacheService):
    async def _get_from_search_engine(self, film_id: str) -> Optional[Film]:
        doc = await self.search_engine.get_data(schema="filmwork", id=film_id)
        if not doc:
            return None
        return Film(**doc)

    async def _get_from_redis(self, composite_id: str) -> Optional[Film]:
        data = await self.redis.get_data(composite_id)

        if not data:
            logging.debug("No data in Redis")
            return None

        logging.debug("Data has been found in Redis")
        film = Film.parse_raw(data)
        return film

    async def _put_to_redis(self, composite_id: str, film: Film):
        result = await self.redis.set_data(
            composite_id, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS
        )
        logging.debug("Put data to Redis")
        logging.debug("Result: %s", result)


class FilmsAllService(BaseService):
    async def _get_from_search_engine(
        self, page: int, size: int, sort: str = None, sort_order: str = None
    ) -> Optional[dict]:
        result = await self.search_engine.get_data(
            index="filmwork",
            query="",
            param_name="",
            page_size=size,
            page_number=page * size,
            sort=f"{sort}:{sort_order}",
        )
        if not result:
            return None

        all_hits = result.get("hits")
        response = []

        if result.get("total") and result["total"].get("value"):
            total_docs = result["total"]["value"]
        else:
            total_docs = 0

        for num, doc in enumerate(all_hits):
            response.append(Film(**doc["_source"]))
        return {
            "total": total_docs,
            "films": response,
        }


class SearchFilmService(BaseService):
    async def _get_from_search_engine(
        self, query: str, page: int, size: int
    ) -> Optional[dict[str, Union[Union[list[Film], int], Any]]]:
        result = await self.search_engine.get_data(
            index="filmwork",
            query=query,
            param_name="title",
            page_number=page * size,
            page_size=size,
        )
        if not result:
            return None

        if result.get("total") and result["total"].get("value"):
            total_docs = result["total"]["value"]
        else:
            total_docs = 0

        films = []
        all_hits = result.get("hits")
        if len(all_hits) > 0:
            if len(all_hits) > 1:
                for num, doc in enumerate(all_hits):
                    films.append(Film(**doc["_source"]))
            else:
                films.append(Film(**all_hits[0]["_source"]))
        return {
            "total": total_docs,
            "films": films,
        }


@lru_cache()
def get_film_service(
    redis: RedisManageData = Depends(get_redis_data),
    search_engine: ElasticGetDataMixin = Depends(get_elastic_data),
) -> FilmService:
    return FilmService(redis, search_engine)


@lru_cache()
def get_all_films_service(
    redis: RedisManageData = Depends(get_redis_data),
    search_engine: ElasticGetDataMixin = Depends(get_elastic_data),
) -> FilmsAllService:
    return FilmsAllService(redis, search_engine)


@lru_cache()
def search_film_service(
    redis: RedisManageData = Depends(get_redis_data),
    search_engine: ElasticGetDataMixin = Depends(get_elastic_data),
) -> SearchFilmService:
    return SearchFilmService(redis, search_engine)
