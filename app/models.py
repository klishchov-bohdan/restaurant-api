import datetime
from decimal import Decimal

from sqlalchemy import (
    TIMESTAMP,
    ForeignKey,
    Integer,
    Text,
    func,
    outerjoin,
    select,
    text,
)
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship

from app.database import Base
from app.schemas import BaseInfoSchema, DishSchema, MenuSchema, SubmenuSchema


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
    dishes: Mapped[list['Dish']] = relationship(back_populates='submenu', single_parent=True, lazy='joined')
    menu: Mapped['Menu'] = relationship(back_populates='submenus', single_parent=True)
    time_created: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    time_updated: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'),
                                                   onupdate=text('CURRENT_TIMESTAMP'))

    dishes_count: Mapped[int] = column_property(
        select(func.count(Dish.id))
        .where(Dish.submenu_id == id)
        .correlate_except(Dish)
        .scalar_subquery()
    )

    def to_base_schema(self) -> BaseInfoSchema:
        return BaseInfoSchema(
            id=self.id,
            title=self.title,
            description=self.description,
        )

    def to_schema(self) -> SubmenuSchema:
        return SubmenuSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            dishes=self.dishes,
            dishes_count=self.dishes_count
        )


class Menu(Base):
    __tablename__ = 'menu'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    submenus: Mapped[list['Submenu']] = relationship(
        load_on_pending=True, back_populates='menu', single_parent=True, lazy='joined')
    time_created: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    time_updated: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'),
                                                   onupdate=text('CURRENT_TIMESTAMP'))

    submenus_count: Mapped[int] = column_property(
        select(func.count(Submenu.id))
        .where(Submenu.menu_id == id)
        .correlate_except(Submenu)
        .scalar_subquery()
    )

    dishes_count: Mapped[int] = column_property(
        select(func.count(Dish.id))
        .select_from(outerjoin(Submenu, Dish, Submenu.id == Dish.submenu_id))
        .where(Submenu.menu_id == id)
        .correlate_except(Dish, Submenu)
        .scalar_subquery()
    )

    def to_base_schema(self) -> BaseInfoSchema:
        return BaseInfoSchema(
            id=self.id,
            title=self.title,
            description=self.description,
        )

    def to_schema(self) -> MenuSchema:
        return MenuSchema(
            id=self.id,
            title=self.title,
            description=self.description,
            submenus=self.submenus,
            submenus_count=self.submenus_count,
            dishes_count=self.dishes_count
        )
