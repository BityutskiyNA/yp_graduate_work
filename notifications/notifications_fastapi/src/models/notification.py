from pydantic import BaseModel


class NotificationByEventType(BaseModel):
    type_id: int


class NotificationRegisteredUser(BaseModel):
    user_id: str
    registration_link: str


class NotificationBySpecificEvent(BaseModel):
    type_id: int
    user_id: str


class NotificationData(BaseModel):
    title: str
    text: str
    image: str


class MessageData(BaseModel):
    mailing_type: int
    validation: bool
    time_zone_check: bool
    time_zone: int
    LOGIN: str
    PASSWORD: str
    DOMAIN: str
    SMTP_HOST: str
    SMTP_PORT: int
    Subject: str
    template: str
    data: list


class NotificationByTypeOfMessage(BaseModel):
    data: NotificationData
    message_data: MessageData
