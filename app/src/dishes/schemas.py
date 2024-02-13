from decimal import Decimal

from fastapi.param_functions import Form
from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from typing_extensions import Annotated

from app.redis_conn import redis_sync
from app.schemas import DishSchema


class CreateDishSchema(BaseModel):
    title: Annotated[str, Form()] = Field(default=None)
    description: Annotated[str, Form()] = Field(default=None)
    price: Annotated[Decimal, Form()] = Field(default=None, ge=.01)


class OutDishSchema(DishSchema):
    id: str

    @field_validator('id', mode='before')
    def transform_id_to_str(cls, value: int) -> str:
        return str(value)

    @field_validator('price', mode='before')
    def price_with_fee(cls, value: Decimal, info: FieldValidationInfo) -> Decimal:
        fee = redis_sync.get(f'dish_{info.data["id"]}_fee')
        if fee:
            return Decimal(round(value - (value * Decimal(fee.decode())), 2))
        else:
            return value
