from pydantic import BaseModel
from datetime import date


class PromocodeData(BaseModel):
    name: str
    discount_amount: int
    validity_period: str
    promo_code_type: str
    active: bool
    created: str


class HistoryData(BaseModel):
    name: str
    created: date
    status: str
    description: str
    subscription_id: int
    promo_code_id: int
    promotional_campaign_id: int
    user: str
