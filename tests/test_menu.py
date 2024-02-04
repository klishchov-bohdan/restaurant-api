from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import insert, select

from app.models import Menu
from tests.conftest import async_session_maker_test


class TestMenu:
    async def test_get_all_menus(self, ac: AsyncClient, api: FastAPI):
        stmt = (
            insert(Menu).values(title='title3', description='description3').returning(Menu.id)
        )
        async with async_session_maker_test() as db:
            await db.execute(stmt)
            await db.commit()
        req_url = api.url_path_for('get_all_menus')
        response = await ac.get(req_url, follow_redirects=True)
        assert response.status_code == 200, 'Can`t get all menus'
        assert response.text[0] == '[' and response.text[-1] == ']', 'Response json is not a list'
        async with async_session_maker_test() as db:
            stmt = select(Menu)
            result = await db.execute(stmt)
        menus = [menu[0] for menu in result.all()]
        for idx, menu in enumerate(menus):
            assert str(menu.id) == response.json()[idx]['id'], 'Menu id is not equal'
            assert menu.title == response.json()[idx]['title'], 'Menu title is not equal'
            assert menu.description == response.json()[idx]['description'], 'Menu description is not equal'

    async def test_create(self, ac: AsyncClient, api: FastAPI):
        req_url = api.url_path_for('create_menu')
        response = await ac.post(req_url, follow_redirects=True,
                                 json={
                                     'title': 'title1',
                                     'description': 'description1'
                                 })
        assert response.status_code == 201, 'Can`t create menu'
        assert response.json()['title'], 'Response haven`t a field title'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['description'], 'Response haven`t a field description'
        query = (
            select(Menu).where(Menu.id == int(response.json()['id']))
        )
        async with async_session_maker_test() as db:
            result = await db.execute(query)
            first = result.first()
            menu = first.Menu
        assert str(menu.id) == response.json()['id'], 'Menu id is not equal'
        assert menu.title == response.json()['title'], 'Menu title is not equal'
        assert menu.description == response.json()['description'], 'Menu description is not equal'

    async def test_get_menu(self, ac: AsyncClient, api: FastAPI):
        stmt = (
            insert(Menu).values(title='title1', description='description1').returning(Menu)
        )
        async with async_session_maker_test() as db:
            result = await db.execute(stmt)
            menu = result.fetchone()[0]
            await db.commit()
        req_url = api.url_path_for('get_menu', menu_id=menu.id)
        response = await ac.get(req_url, follow_redirects=True)
        assert response.status_code == 200, 'Can`t get menu by id'
        assert response.json()['id'], 'Response haven`t a field id'
        assert str(menu.id) == response.json()['id'], 'Menu id is not equal'
        assert menu.title == response.json()['title'], 'Menu title is not equal'
        assert menu.description == response.json()['description'], 'Menu description is not equal'

    async def test_update(self, ac: AsyncClient, api: FastAPI):
        req_url = api.url_path_for('update_menu', menu_id=1)
        response = await ac.patch(req_url, follow_redirects=True,
                                  json={
                                      'title': 'new_title',
                                      'description': 'new_description'
                                  })
        assert response.status_code == 200, 'Can`t update menu'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['id'] == '1', 'Invalid menu id response'
        assert response.json()['title'] == 'new_title', 'Invalid menu title response'
        assert response.json()['description'] == 'new_description', 'Invalid menu description response'
        query = (
            select(Menu).where(Menu.id == int(response.json()['id']))
        )
        async with async_session_maker_test() as db:
            result = await db.execute(query)
            first = result.first()
            menu = first.Menu
        assert str(menu.id) == response.json()['id'], 'Menu id is not equal'
        assert menu.title == response.json()['title'], 'Menu title is not equal'
        assert menu.description == response.json()['description'], 'Menu description is not equal'

    async def test_delete(self, ac: AsyncClient, api: FastAPI):
        stmt = (
            insert(Menu).values(title='title1', description='description1').returning(Menu.id)
        )
        async with async_session_maker_test() as db:
            result = await db.execute(stmt)
            menu_id = result.fetchone()[0]
            await db.commit()
        req_url = api.url_path_for('delete_menu', menu_id=menu_id)
        response = await ac.delete(req_url, follow_redirects=True)
        assert response.status_code == 200, 'Can`t delete menu by id'
        assert not response.json(), 'Invalid response'
        query = (
            select(Menu).where(Menu.id == menu_id)
        )
        async with async_session_maker_test() as db:
            result = await db.execute(query)
            first = result.first()
        assert first is None, 'Can`t delete menu'
