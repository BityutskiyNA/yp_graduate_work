from typing import Optional

from .base import BaseClass


class Genre(BaseClass):
    name: str
    description: Optional[str]
