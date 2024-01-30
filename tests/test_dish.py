import re

from httpx import AsyncClient
from sqlalchemy import insert, select

from app.models import Dish
from tests.conftest import async_session_maker_test


class TestDish:
    async def test_get_all_dishes(self, ac: AsyncClient):
        stmt = (
            insert(Dish).values(title='title1', description='description1', price='12.53', submenu_id=1).returning(Dish)
        )
        async with async_session_maker_test() as db:
            result = await db.execute(stmt)
            dish = result.fetchone()[0]
            await db.commit()
        response = await ac.get(f'/menus/1/submenus/1/dishes', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get all dishes'
        assert response.text[0] == '[' and response.text[-1] == ']', 'Response json is not a list'
        async with async_session_maker_test() as db:
            stmt = select(Dish)
            result = await db.execute(stmt)
        dishes = [dish[0] for dish in result.all()]
        for idx, dish in enumerate(dishes):
            assert str(dish.id) == response.json()[idx]['id'], 'Dish id is not equal'
            assert dish.title == response.json()[idx]['title'], 'Dish title is not equal'
            assert str(dish.price) == response.json()[idx]['price'], 'Dish price is not equal'
            assert dish.description == response.json()[idx]['description'], 'Dish description is not equal'

    async def test_create(self, ac: AsyncClient):
        response = await ac.post('/menus/1/submenus/1/dishes', follow_redirects=True,
                                 json={
                                     "title": "title1",
                                     "description": "description1",
                                     "price": "54.12"
                                 })
        assert response.status_code == 201, 'Can`t create dish'
        assert response.json()['title'], 'Response haven`t a field title'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['description'], 'Response haven`t a field description'
        assert response.json()['price'], 'Response haven`t a field price'
        assert re.fullmatch(r'^\d+.\d\d$', response.json()['price'])
        query = (
            select(Dish).where(Dish.id == int(response.json()['id']))
        )
        async with async_session_maker_test() as db:
            result = await db.execute(query)
            first = result.first()
            assert first is not None, 'Can`t create dish'
            dish = first.Dish
        assert str(dish.id) == response.json()['id'], 'Dish id is not equal'
        assert dish.title == response.json()['title'], 'Dish title is not equal'
        assert dish.description == response.json()['description'], 'Dish description is not equal'
        assert str(dish.price) == response.json()['price'], 'Dish title is not equal'

    async def test_get_dish(self, ac: AsyncClient):
        stmt = (
            insert(Dish).values(title='title1', description='description1', price='12.63', submenu_id=1).returning(Dish)
        )
        async with async_session_maker_test() as db:
            result = await db.execute(stmt)
            dish = result.fetchone()[0]
            await db.commit()
        response = await ac.get(f'/menus/1/submenus/1/dishes/{dish.id}', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get dish by id'
        assert response.json()['title'], 'Response haven`t a field title'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['description'], 'Response haven`t a field description'
        assert response.json()['price'], 'Response haven`t a field price'
        assert response.json()['id'] == str(dish.id), 'Invalid dish response'
        assert re.fullmatch(r'^\d+.\d\d$', response.json()['price'])
        query = (
            select(Dish).where(Dish.id == int(response.json()['id']))
        )
        async with async_session_maker_test() as db:
            result = await db.execute(query)
            first = result.first()
            assert first is not None, 'Can`t get dish'
            dish = first.Dish
        assert str(dish.id) == response.json()['id'], 'Dish id is not equal'
        assert dish.title == response.json()['title'], 'Dish title is not equal'
        assert dish.description == response.json()['description'], 'Dish description is not equal'
        assert str(dish.price) == response.json()['price'], 'Dish title is not equal'

    async def test_update(self, ac: AsyncClient):
        stmt = (
            insert(Dish).values(title='title1', description='description1', price='12.53', submenu_id=1).returning(Dish)
        )
        async with async_session_maker_test() as db:
            result = await db.execute(stmt)
            dish = result.fetchone()[0]
            await db.commit()
        response = await ac.patch(f'/menus/1/submenus/1/dishes/{dish.id}', follow_redirects=True,
                                  json={
                                      'title': 'new_title',
                                      'description': 'new_description',
                                      'price': '12.65'
                                  })
        assert response.status_code == 200, 'Can`t update dish'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['id'] == str(dish.id), 'Invalid dish id response'
        assert response.json()['title'] == 'new_title', 'Invalid dish title response'
        assert response.json()['description'] == 'new_description', 'Invalid dish description response'
        assert response.json()['price'] == '12.65', 'Invalid dish price response'
        query = (
            select(Dish).where(Dish.id == int(response.json()['id']))
        )
        async with async_session_maker_test() as db:
            result = await db.execute(query)
            first = result.first()
            assert first is not None, 'Can`t update dish'
            dish = first.Dish
        assert str(dish.id) == response.json()['id'], 'Dish id is not equal'
        assert dish.title == response.json()['title'], 'Dish title is not equal'
        assert dish.description == response.json()['description'], 'Dish description is not equal'
        assert str(dish.price) == response.json()['price'], 'Dish title is not equal'

    async def test_delete(self, ac: AsyncClient):
        stmt = (
            insert(Dish).values(title='title1', description='description1', price='43.12', submenu_id=1).returning(Dish.id)
        )
        async with async_session_maker_test() as db:
            result = await db.execute(stmt)
            dish_id = result.fetchone()[0]
            await db.commit()
        response = await ac.delete(f'/menus/1/submenus/1/dishes/{dish_id}', follow_redirects=True)
        assert response.status_code == 200, 'Can`t delete dish by id'
        assert not response.json(), 'Invalid response'
        query = (
            select(Dish).where(Dish.id == dish_id)
        )
        async with async_session_maker_test() as db:
            result = await db.execute(query)
            first = result.first()
        assert first is None, 'Can`t delete dish'
