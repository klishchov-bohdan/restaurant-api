from fastapi.param_functions import Form
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated

from app.schemas import BaseInfoSchema, SubmenuSchema


class CreateSubmenuSchema(BaseModel):
    title: Annotated[str, Form()] = Field(default=None)
    description: Annotated[str, Form()] = Field(default=None)


class OutSubmenuSchema(SubmenuSchema):
    id: str
    dishes_count: int

    @field_validator('id', mode='before')
    def transform_id_to_str(cls, value: int) -> str:
        return str(value)


class OutModifiedSchema(BaseInfoSchema):
    id: str

    @field_validator('id', mode='before')
    def transform_id_to_str(cls, value: int) -> str:
        return str(value)
