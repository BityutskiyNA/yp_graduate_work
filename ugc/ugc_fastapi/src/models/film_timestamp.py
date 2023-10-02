from uuid import UUID

from pydantic import BaseModel


class FilmTimestamp(BaseModel):
    user_id: UUID
    film_id: UUID
    time_watched: float
