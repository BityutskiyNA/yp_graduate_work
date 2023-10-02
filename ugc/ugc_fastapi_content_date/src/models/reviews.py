from pydantic import BaseModel


class Review(BaseModel):
    user_id: str
    movies_id: str
    review_id: str
    review_text: str
