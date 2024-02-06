from typing import Any

from app.models import Dish
from app.utils.repository import SQLAlchemyRepository


class DishRepository(SQLAlchemyRepository):
    model: Any = Dish
