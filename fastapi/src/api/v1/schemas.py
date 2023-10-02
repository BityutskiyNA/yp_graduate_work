from typing import Any, Optional

from pydantic import BaseModel


class PaginatedPage(BaseModel):
    items: list[Any]
    first: int
    last: int
    prev: Optional[int]
    next: Optional[int]
