from app.models import Dish
from app.utils.repository import SQLAlchemyRepository


class DishRepository(SQLAlchemyRepository):
    model = Dish
