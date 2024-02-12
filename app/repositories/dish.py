from typing import Any

from app.database import Base
from app.models import Dish
from app.utils.repository import SQLAlchemyRepository


class DishRepository(SQLAlchemyRepository):
    model: Any = Dish
    base_returning_model: Any = type('BaseReturningModel', (Base,), {
        '__tablename__': Dish.__tablename__,
        'id': Dish.id,
        'title': Dish.title,
        'description': Dish.description,
        'price': Dish.price,
        'to_base_schema': Dish.to_schema
    })
