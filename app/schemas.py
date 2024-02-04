from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class DishSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | str
    title: str
    description: str
    price: Decimal = Field(ge=.01)


class SubmenuSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | str
    title: str
    description: str
    dishes_count: int
    dishes: list[DishSchema] | None


class MenuSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int | str
    title: str
    description: str
    submenus_count: int
    dishes_count: int
    submenus: list[SubmenuSchema] | None
