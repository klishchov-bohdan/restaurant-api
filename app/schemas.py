from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from app.redis_conn import redis_sync


class BaseInfoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | str
    title: str
    description: str


class DishSchema(BaseInfoSchema):
    price: Decimal = Field(ge=.01)

    @field_validator('price', mode='before')
    def price_with_fee(cls, value: Decimal, info: FieldValidationInfo) -> Decimal:
        fee = redis_sync.get(f'dish_{info.data["id"]}_fee')
        if fee:
            return Decimal(round(value - (value * Decimal(fee.decode())), 2))
        else:
            return value


class SubmenuSchema(BaseInfoSchema):
    dishes_count: int
    dishes: list[DishSchema] | None


class MenuSchema(BaseInfoSchema):
    submenus_count: int
    dishes_count: int
    submenus: list[SubmenuSchema] | None
