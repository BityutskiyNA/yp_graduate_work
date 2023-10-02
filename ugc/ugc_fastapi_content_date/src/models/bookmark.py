from pydantic import BaseModel


class Bookmark(BaseModel):
    user_id: str
    movies_id: str
