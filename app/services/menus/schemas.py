from pydantic import BaseModel, Field, validator, ConfigDict, field_validator
from typing_extensions import Annotated
from fastapi.param_functions import Form

from app.schemas import MenuSchema


class CreateMenuSchema(BaseModel):
    title: Annotated[str, Form()] = Field(default=None)
    description: Annotated[str, Form()] = Field(default=None)


class OutMenuSchema(MenuSchema):
    id: str
    submenus_count: int
    dishes_count: int

    @field_validator("id", mode='before')
    def transform_id_to_str(cls, value) -> str:
        return str(value)
