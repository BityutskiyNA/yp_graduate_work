from dataclasses import dataclass
from datetime import datetime


@dataclass
class PayloadDataclass:
    id: str
    session_id: str
    is_admin: bool
    is_refresh: bool
    exp: datetime
    token: str

    def __post_init__(self):
        assert self.id is not None, "id cant be None"
        assert self.session_id is not None, "session_id cant be None"
        assert self.is_admin is not None, "is_admin cant be None"
        assert self.is_refresh is not None, "is_refresh cant be None"
        assert self.exp is not None, "exp cant be None"
        assert self.token is not None, "token cant be None"
