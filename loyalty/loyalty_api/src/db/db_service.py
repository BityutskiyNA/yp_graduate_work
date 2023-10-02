import json
import os
from datetime import date
from typing import Generator

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from src.core.config import app_settings
from src.models.loyalty import HistoryData


engine = sqlalchemy.create_engine(app_settings.url, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

Base = automap_base()
Base.prepare(engine, reflect=True)

Promocode = Base.classes.discount_promocode
PromotionalCampaign = Base.classes.discount_promotionalcampaign
History = Base.classes.discount_discount_history


def as_dict(obj: object) -> dict:
    data = obj.__dict__
    data.pop("_sa_instance_state")
    return data


Promocode.as_dict = as_dict
PromotionalCampaign.as_dict = as_dict
History.as_dict = as_dict


def get_db() -> Generator:
    db = Session()
    try:
        yield db
    finally:
        db.close()


def get_all_promocodes(db: Session, limit: int, page: int) -> dict | None:
    """Получение всех промокодов"""
    skip = (page - 1) * limit
    promocodes = db.query(Promocode).limit(limit).offset(skip).all()
    if promocodes:
        promocodes_dict = [record.as_dict() for record in promocodes]
        return {
            "status": "success",
            "results": len(promocodes),
            "promocodes": promocodes_dict,
        }
    return None


def get_all_promocodes_by_campaign(
    db: Session, limit: int, page: int, campaign_id: str
) -> dict | None:
    """Получение всех промокодов по акции (промо-кампании)"""
    skip = (page - 1) * limit
    promocodes = (
        db.query(Promocode)
        .filter_by(promotional_campaign_id=campaign_id)
        .limit(limit)
        .offset(skip)
        .all()
    )
    if promocodes:
        promocodes_dict = [record.as_dict() for record in promocodes]
        return {
            "status": "success",
            "results": len(promocodes),
            "promocodes": promocodes_dict,
        }
    return None


def get_campaign_info_by_promocode(promocode: str, db: Session) -> dict | None:
    """Получение информации об акции (промо-кампании) по промокоду"""
    promocode = db.query(Promocode).filter_by(name=promocode).first()
    if promocode:
        campaign_info = (
            db.query(PromotionalCampaign)
            .filter_by(id=promocode.promotional_campaign_id)
            .first()
        )
        campaign_info_dict = campaign_info.as_dict()
        promocode_dict = promocode.as_dict()
        return {
            "status": "success",
            "campaign_info": campaign_info_dict,
            "promocode_info": promocode_dict,
        }
    return None


def get_promocode_info(promocode_id: int, db: Session) -> Promocode:
    promocode = db.query(Promocode).filter_by(id=promocode_id).first()
    return promocode


def set_promocode_used(promocode_name: str, db: Session) -> bool:
    promocode = db.query(Promocode).filter_by(name=promocode_name).first()
    promocode.active = False
    db.commit()
    return True


def add_promocode_history(history: HistoryData, db: Session) -> None:
    """Добавление записи в историю использования промокодов"""
    new_record = History(
        name=history.name,
        created=history.created,
        status=history.status,
        description=history.description,
        subscription_id=history.subscription_id,
        promo_code_id=history.promo_code_id,
        promotional_campaign_id=history.promotional_campaign_id,
        user=history.user,
    )
    db.add(new_record)
    db.commit()


class DateEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)
