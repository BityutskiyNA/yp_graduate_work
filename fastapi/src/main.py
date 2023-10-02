import logging

import uvicorn
from api.v1 import films, genres, persons
from core import base_config as config
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

log = logging.getLogger(__name__)

tags_metadata = [
    {
        "name": config.project_name,
        "description": "Получение информации о фильмах",
    },
]

app = FastAPI(
    title="Read-only API для онлайн-кинотеатра",
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    openapi_tags=tags_metadata,
)


@app.on_event("startup")
async def startup():
    log.info("Startup ....")
    redis.red.set_db(Redis(host=config.redis_film_host, port=config.redis_film_port))
    elastic.es.set_db(
        AsyncElasticsearch(hosts=[f"{config.elastic_host}:{config.elastic_port}"])
    )


@app.on_event("shutdown")
async def shutdown():
    log.info("Shutdown ....")
    await redis.red.db.close()
    await elastic.es.db.close()


# Подключаем роутер к серверу, указав префикс /v1/films
# Теги указываем для удобства навигации по документации
app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        log_level="info",
        debug=True,
        reload=True,
    )
