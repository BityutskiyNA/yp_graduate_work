from dataclasses import dataclass
from datetime import datetime


@dataclass
class AuthDataclass:
    login: str
    password: str
    social_id: str
    email: str

    def __post_init__(self):
        assert self.login is not None, "Login cant be None"
        assert self.password is not None, "Password cant be None"
        assert len(self.login) != 0, "Login cant be blank"
        assert len(self.password) != 0, "Password cant be blank"
