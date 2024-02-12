from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class BaseInfoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | str
    title: str
    description: str


class DishSchema(BaseInfoSchema):
    price: Decimal = Field(ge=.01)


class SubmenuSchema(BaseInfoSchema):
    dishes_count: int
    dishes: list[DishSchema] | None


class MenuSchema(BaseInfoSchema):
    submenus_count: int
    dishes_count: int
    submenus: list[SubmenuSchema] | None
