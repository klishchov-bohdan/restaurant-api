from fastapi.param_functions import Form
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated

from app.schemas import MenuSchema


class CreateMenuSchema(BaseModel):
    title: Annotated[str, Form()] = Field(default=None)
    description: Annotated[str, Form()] = Field(default=None)


class OutMenuSchema(MenuSchema):
    id: str

    @field_validator('id', mode='before')
    def transform_id_to_str(cls, value) -> str:
        return str(value)
