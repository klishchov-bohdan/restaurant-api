from app.models import Menu
from app.utils.repository import SQLAlchemyRepository


class MenuRepository(SQLAlchemyRepository):
    model = Menu
