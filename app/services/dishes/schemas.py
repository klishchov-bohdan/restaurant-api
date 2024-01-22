from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated
from fastapi.param_functions import Form
from decimal import Decimal

from app.schemas import DishSchema


class CreateDishSchema(BaseModel):
    title: Annotated[str, Form()] = Field(default=None)
    description: Annotated[str, Form()] = Field(default=None)
    price: Annotated[Decimal, Form()] = Field(default=None)


class OutDishSchema(DishSchema):
    id: str

    @field_validator("id", mode='before')
    def transform_id_to_str(cls, value) -> str:
        return str(value)
