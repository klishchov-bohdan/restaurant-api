import datetime
from decimal import Decimal

from sqlalchemy import TIMESTAMP, ForeignKey, Integer, Text, text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.schemas import DishSchema, MenuSchema, SubmenuSchema


class Dish(Base):
    __tablename__ = 'dish'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(nullable=False)
    submenu_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        'submenu.id', ondelete='CASCADE'), nullable=False)
    submenu: Mapped['Submenu'] = relationship(back_populates='dishes', single_parent=True)
    time_created: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    time_updated: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'),
                                                   onupdate=text('CURRENT_TIMESTAMP'))

    def to_schema(self) -> DishSchema:
        return DishSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            price=self.price
        )


class Submenu(Base):
    __tablename__ = 'submenu'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    menu_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        'menu.id', ondelete='CASCADE'), nullable=False)
    dishes: Mapped[list['Dish']] = relationship(back_populates='submenu', single_parent=True, lazy='selectin')
    menu: Mapped['Menu'] = relationship(back_populates='submenus', single_parent=True)
    time_created: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    time_updated: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'),
                                                   onupdate=text('CURRENT_TIMESTAMP'))

    @hybrid_property
    def dishes_count(self):
        return len(self.dishes)

    def to_schema(self) -> SubmenuSchema:
        return SubmenuSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            dishes_count=self.dishes_count,
            dishes=[dish.to_schema() for dish in self.dishes]
        )


class Menu(Base):
    __tablename__ = 'menu'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    submenus: Mapped[list['Submenu']] = relationship(back_populates='menu', single_parent=True, lazy='selectin')
    time_created: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    time_updated: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'),
                                                   onupdate=text('CURRENT_TIMESTAMP'))

    @hybrid_property
    def submenus_count(self):
        return len(self.submenus)

    @hybrid_property
    def dishes_count(self):
        return sum(submenu.dishes_count for submenu in self.submenus)

    def to_schema(self) -> MenuSchema:
        return MenuSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            submenus_count=self.submenus_count,
            dishes_count=self.dishes_count,
            submenus=[submenu.to_schema() for submenu in self.submenus]
        )
