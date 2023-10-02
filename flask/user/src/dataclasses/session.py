from dataclasses import dataclass
from datetime import datetime


@dataclass
class SessionDataclass:
    user_id: str
    user_agent: str
