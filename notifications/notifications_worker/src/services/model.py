from pydantic import BaseModel
from typing import Optional


class DataMailData(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None


class DataMail(BaseModel):
    mailing_type: Optional[str] = None
    agent: Optional[str] = 'mail'
    validation: Optional[bool] = False
    event_type: Optional[str] = None
    fio: Optional[str] = None
    email: Optional[str] = None
    time_zone_check: Optional[bool] = False
    time_zone: Optional[int] = None
    login: Optional[str] = None
    password: Optional[str] = None
    domain: Optional[str] = None
    smtp_host: Optional[str] = None
    smtp_port: Optional[str] = None
    sender: Optional[str] = None
    api_key: Optional[str] = None
    subject: Optional[str] = None
    template: Optional[str] = None
    data: Optional[DataMailData] = None

    def to_json(self) -> str:
        return self.json()



class DataWebPuch(BaseModel):
    mailing_type: Optional[str] = None
    api_token: Optional[str] = None

    def to_json(self) -> str:
        return self.json()