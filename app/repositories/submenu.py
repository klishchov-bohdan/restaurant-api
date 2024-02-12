from typing import Any

from app.database import Base
from app.models import Submenu
from app.utils.repository import SQLAlchemyRepository


class SubmenuRepository(SQLAlchemyRepository):
    model: Any = Submenu
    base_returning_model: Any = type('BaseReturningModel', (Base,), {
        '__tablename__': Submenu.__tablename__,
        'id': Submenu.id,
        'title': Submenu.title,
        'description': Submenu.description,
        'to_base_schema': Submenu.to_base_schema
    })
