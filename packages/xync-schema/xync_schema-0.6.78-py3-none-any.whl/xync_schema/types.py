from datetime import datetime
from pydantic import BaseModel, Field

from xync_schema.enums import AdStatus, OrderStatus
from xync_schema import models


class UnitEx(BaseModel):
    exid: int | str
    ticker: str
    scale: int = None
    rate: float | None = None


class CoinEx(UnitEx):
    p2p: bool = None
    minimum: float | None = None


class CurEx(UnitEx):
    rounding_scale: int | None = None
    minimum: int | None = None


class PmexBank(BaseModel):
    # id: int | None = None
    exid: str
    name: str


# class Pmcur(Struct):
#     id: int | None = None
#     pm_id: int
#     cur_id: int


class BaseAd(BaseModel):
    price: float
    exid: int | None = Field(alias="id")


class BaseAdIn(BaseAd):
    min_fiat: float
    max_fiat: float
    direction: models.Direction
    detail: str | None = None
    auto_msg: str | None = None
    status: AdStatus = AdStatus.active
    maker: models.Actor = None
    _unq = "exid", "maker", "direction"

    class Config:
        arbitrary_types_allowed = True


class AdBuyIn(BaseAdIn):
    pms_: list[models.Pm]


class AdSaleIn(BaseAdIn):
    creds_: list[models.Cred]


class BaseOrder(BaseModel):
    id: int | None = None


class OrderIn(BaseModel):
    exid: int
    amount: float
    created_at: datetime
    ad: models.Ad
    cred: models.Cred
    taker: models.Actor
    id: int = None
    maker_topic: int | None = None
    taker_topic: int | None = None
    status: OrderStatus = OrderStatus.created
    payed_at: datetime | None = None
    confirmed_at: datetime | None = None
    appealed_at: datetime | None = None
    _unq = "id", "exid", "amount", "maker_topic", "taker_topic", "ad", "cred", "taker"

    class Config:
        arbitrary_types_allowed = True
