from pydantic import BaseModel


class Сomment(BaseModel):
    user_id: str
    movies_id: str
    comment_id: str
    comment_text: str
