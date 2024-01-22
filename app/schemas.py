from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, validator, ConfigDict
from typing_extensions import Annotated
from fastapi.param_functions import Form


class DishSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    price: Decimal


class SubmenuSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    dishes: Optional[list[DishSchema]]


class MenuSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    submenus: Optional[list[SubmenuSchema]]

