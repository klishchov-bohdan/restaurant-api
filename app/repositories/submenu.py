from app.models import Submenu
from app.utils.repository import SQLAlchemyRepository


class SubmenuRepository(SQLAlchemyRepository):
    model = Submenu
