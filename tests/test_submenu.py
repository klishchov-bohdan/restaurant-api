from httpx import AsyncClient
from sqlalchemy import insert, select

from app.models import Submenu
from tests.conftest import async_session_maker_test


class TestSubmenu:
    async def test_get_all_submenus(self, ac: AsyncClient):
        stmt = (
            insert(Submenu).values(title='title1', description='description1', menu_id=1).returning(Submenu)
        )
        async with async_session_maker_test() as db:
            result = await db.execute(stmt)
            submenu = result.fetchone()[0]
            await db.commit()
        response = await ac.get(f'/menus/{submenu.menu_id}/submenus', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get all submenus'
        assert response.text[0] == '[' and response.text[-1] == ']', 'Response json is not a list'
        async with async_session_maker_test() as db:
            stmt = select(Submenu)
            result = await db.execute(stmt)
        submenus = [submenu[0] for submenu in result.all()]
        for idx, submenu in enumerate(submenus):
            assert str(submenu.id) == response.json()[idx]['id'], 'Submenu id is not equal'
            assert submenu.title == response.json()[idx]['title'], 'Submenu title is not equal'
            assert submenu.description == response.json()[idx]['description'], 'Submenu description is not equal'

    async def test_create(self, ac: AsyncClient):
        response = await ac.post('/menus/1/submenus', follow_redirects=True,
                                 json={
                                     "title": "title1",
                                     "description": "description1"
                                 })
        assert response.status_code == 201, 'Can`t create submenu'
        assert response.json()['title'], 'Response haven`t a field title'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['description'], 'Response haven`t a field description'
        query = (
            select(Submenu).where(Submenu.id == int(response.json()['id']))
        )
        async with async_session_maker_test() as db:
            result = await db.execute(query)
            first = result.first()
            assert first is not None, 'Can`t create submenu'
            submenu = first.Submenu
        assert str(submenu.id) == response.json()['id'], 'Submenu id is not equal'
        assert submenu.title == response.json()['title'], 'Submenu title is not equal'
        assert submenu.description == response.json()['description'], 'Submenu description is not equal'

    async def test_get_submenu(self, ac: AsyncClient):
        stmt = (
            insert(Submenu).values(title='title1', description='description1', menu_id=1).returning(Submenu)
        )
        async with async_session_maker_test() as db:
            result = await db.execute(stmt)
            submenu = result.fetchone()[0]
            await db.commit()
        response = await ac.get(f'/menus/1/submenus/{submenu.id}', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get submenu by id'
        assert response.json()['id'], 'Response haven`t a field id'
        assert str(submenu.id) == response.json()['id'], 'Submenu id is not equal'
        assert submenu.title == response.json()['title'], 'Submenu title is not equal'
        assert submenu.description == response.json()['description'], 'Submenu description is not equal'

    async def test_update(self, ac: AsyncClient):
        response = await ac.patch('/menus/1/submenus/1', follow_redirects=True,
                                  json={
                                      'title': 'new_title',
                                      'description': 'new_description'
                                  })
        assert response.status_code == 200, 'Can`t update submenu'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['id'] == '1', 'Invalid submenu id response'
        assert response.json()['title'] == 'new_title', 'Invalid submenu title response'
        assert response.json()['description'] == 'new_description', 'Invalid submenu description response'
        query = (
            select(Submenu).where(Submenu.id == int(response.json()['id']))
        )
        async with async_session_maker_test() as db:
            result = await db.execute(query)
            first = result.first()
            assert first is not None, 'Updating error'
            submenu = first.Submenu
        assert str(submenu.id) == response.json()['id'], 'Submenu id is not equal'
        assert submenu.title == response.json()['title'], 'Submenu title is not equal'
        assert submenu.description == response.json()['description'], 'Submenu description is not equal'

    async def test_delete(self, ac: AsyncClient):
        stmt = (
            insert(Submenu).values(title='title1', description='description1', menu_id=1).returning(Submenu.id)
        )
        async with async_session_maker_test() as db:
            result = await db.execute(stmt)
            submenu_id = result.fetchone()[0]
            await db.commit()
        response = await ac.delete(f'/menus/1/submenus/{submenu_id}', follow_redirects=True)
        assert response.status_code == 200, 'Can`t delete submenu by id'
        assert not response.json(), 'Invalid response'
        query = (
            select(Submenu).where(Submenu.id == submenu_id)
        )
        async with async_session_maker_test() as db:
            result = await db.execute(query)
            first = result.first()
        assert first is None, 'Can`t delete menu'
