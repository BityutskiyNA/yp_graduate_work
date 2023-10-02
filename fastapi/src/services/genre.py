import json
import logging
from functools import lru_cache
from typing import Optional

from db.elastic import ElasticGetDataMixin, get_elastic_data
from db.redis import RedisManageData, get_redis_data
from models.genre import Genre
from services.base_service import BaseCacheService, BaseService

from fastapi import Depends

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут
GENRE_PER_PAGE = 10
GENRE_PER_SEARCH = 3


class GenreService(BaseCacheService):
    async def _get_from_search_engine(self, id: str) -> Optional[Genre]:
        doc = await self.search_engine.get_data(schema="genre", id=id)
        if not doc:
            return None
        return Genre(**doc)

    async def _get_from_redis(self, composite_id: str) -> Optional[Genre]:
        data = await self.redis.get_data(composite_id)
        if not data:
            logging.debug("No data in Redis")
            return None

        logging.debug("Data has been found in Redis")
        genre = Genre.parse_raw(data)
        return genre

    async def _put_to_redis(self, composite_id, genre: Genre):
        logging.debug("Put data to Redis")
        result = await self.redis.set_data(
            key=composite_id, value=genre.json(), expires=GENRE_CACHE_EXPIRE_IN_SECONDS
        )
        logging.debug("Result: %s", result)


class SearchGenreService(BaseService):
    async def _get_from_search_engine(self, query: str) -> Optional[Genre]:
        result = await self.search_engine.get_data(
            index="genre",
            query=query,
            param_name="name",
            page_number=0,
            page_size=GENRE_PER_SEARCH,
        )
        if not result:
            return None
        all_hits = result.get("hits")

        if len(all_hits) > 0:
            if len(all_hits) > 1:
                for num, doc in enumerate(all_hits):
                    return Genre(**doc["_source"])
            else:
                return Genre(**all_hits[0]["_source"])
        else:
            return None


class GenreAllService(BaseCacheService):
    async def _get_from_search_engine(
        self,
        page: int,
        size: int,
    ) -> Optional[dict[str, list]]:
        result = await self.search_engine.get_data(
            index="genre",
            query="",
            param_name="",
            page_number=page,
            page_size=size,
            track_total_hits=True,
        )
        if not result:
            return None
        if result.get("total") and result["total"].get("value"):
            total_docs = result["total"]["value"]
        else:
            total_docs = 0

        all_hits = result["hits"]
        response = []

        for num, doc in enumerate(all_hits):
            response.append(doc["_source"])
        return {
            "total": total_docs,
            "genres": response,
        }

    async def _get_from_redis(self, composite_id: str) -> Optional[dict[str, list]]:
        data = await self.redis.get_dataset(composite_id)
        if not data:
            logging.debug("No data in Redis")
            return None

        logging.debug("Data has been found in Redis")
        genres: list[dict] = []
        for raw_genre in data:
            genres.append(json.loads(raw_genre))
            logging.debug(json.loads(raw_genre))
        return {
            "total": len(genres),
            "genres": genres,
        }

    async def _put_to_redis(self, composite_id, data: dict):
        await self.redis.delete_and_push_dict(
            composite_id=composite_id,
            data_dict=data,
            match="all_genre*",
            field="genres",
        )


@lru_cache()
def get_genre_service(
    redis: RedisManageData = Depends(get_redis_data),
    search_engine: ElasticGetDataMixin = Depends(get_elastic_data),
) -> GenreService:
    return GenreService(redis, search_engine)


@lru_cache()
def get_genre_all_service(
    redis: RedisManageData = Depends(get_redis_data),
    search_engine: ElasticGetDataMixin = Depends(get_elastic_data),
) -> GenreAllService:
    return GenreAllService(redis, search_engine)


@lru_cache()
def search_genre_service(
    redis: RedisManageData = Depends(get_redis_data),
    search_engine: ElasticGetDataMixin = Depends(get_elastic_data),
) -> SearchGenreService:
    return SearchGenreService(redis, search_engine)
