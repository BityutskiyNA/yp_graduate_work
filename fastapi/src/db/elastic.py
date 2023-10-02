from typing import Any, Optional

from db.base_db import AbstractDBBase, AbstractDBGetData
from elasticsearch import AsyncElasticsearch, NotFoundError


class ElasticBase(AbstractDBBase):
    def __init__(self):
        self.db: Optional[AsyncElasticsearch] = None

    def set_db(self, db: AsyncElasticsearch) -> None:
        self.db = db

    async def close(self):
        await self.db.close()


class ElasticGetDataBase(ElasticBase, AbstractDBGetData):
    def __init__(self, elastic_instance: ElasticBase):
        super().__init__()
        self.db = elastic_instance.db

    async def get_data(self, *args, **kwargs):
        pass


class ElasticGetByIdMixin(ElasticGetDataBase):
    async def get_data(self, schema: str, id: str):
        try:
            doc = await self.db.get(schema, id)
        except NotFoundError:
            return None

        return doc.get("_source")


class ElasticGetManyMixin(ElasticGetDataBase):
    async def get_data(self, schema: str, ids: list[str]):
        try:
            docs = await self.db.mget(index=schema, body={"ids": ids})
        except NotFoundError:
            return None
        return docs.get("docs")


class ElasticSearchMixin(ElasticGetDataBase):
    ElasticsearchQuery = Any

    def _make_text_query(
        self, query: str, param_name: str = "name"
    ) -> ElasticsearchQuery:
        return {
            "fuzzy": {
                param_name: {
                    "value": query,
                }
            }
        }

    # "query": {"match": {"name": {"query": query, "fuzziness": "auto"}}}

    _match_all_query: ElasticsearchQuery = {"match_all": {}}

    def _get_body(
        self,
        query: str,
        param_name: str,
        page_size: int,
        page_number: Optional[int] = None,
        track_total_hits: Optional[bool] = True,
    ):
        body = {
            "track_total_hits": track_total_hits,
            "query": self._make_text_query(query, param_name)
            if query
            else self._match_all_query,
            "size": page_size,
        }
        if page_number:
            body["from"] = page_number * page_size
        return body

    async def get_data(
        self,
        index: str,
        query: str,
        param_name: str,
        page_size: int,
        page_number: Optional[int] = None,
        sort: str = "",
        track_total_hits: Optional[bool] = True,
        body: Optional[dict] = None,
    ):
        if not body:
            body = self._get_body(
                query,
                param_name,
                page_size,
                page_number,
                track_total_hits,
            )
        try:
            docs = await self.db.search(
                index=index, body=body, sort=sort if sort else ""
            )
        except NotFoundError:
            return None
        if not docs:
            return None
        return docs.get("hits")


class ElasticGetDataMixin(ElasticGetByIdMixin, ElasticGetManyMixin, ElasticSearchMixin):
    async def get_data(self, *args, **kwargs):
        if "id" in kwargs:
            return await ElasticGetByIdMixin.get_data(
                self, schema=kwargs["schema"], id=kwargs["id"]
            )
        elif "ids" in kwargs:
            return await ElasticGetManyMixin.get_data(
                self, schema=kwargs["schema"], ids=kwargs["ids"]
            )
        elif "index" in kwargs:
            return await ElasticSearchMixin.get_data(self, *args, **kwargs)


def get_elastic_data() -> ElasticGetDataMixin:
    return ElasticGetDataMixin(es)


es = ElasticBase()
