from datetime import datetime

from pydantic import BaseModel


class State(BaseModel):
    updated_at: datetime
