from typing import Any

from app.database import Base
from app.models import Menu
from app.utils.repository import SQLAlchemyRepository


class MenuRepository(SQLAlchemyRepository):
    model: Any = Menu
    base_returning_model: Any = type('BaseReturningModel', (Base, ), {
        '__tablename__': Menu.__tablename__,
        'id': Menu.id,
        'title': Menu.title,
        'description': Menu.description,
        'to_base_schema': Menu.to_base_schema
    })
