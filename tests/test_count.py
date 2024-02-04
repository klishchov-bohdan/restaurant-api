from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import select

from app.models import Dish, Menu, Submenu
from tests.conftest import async_session_maker_test


class TestDishesAndSubmenusCount:
    async def test_submenus_and_dishes_count(self, ac: AsyncClient, api: FastAPI):
        # Create menu
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

        # Create submenu
        req_url = api.url_path_for('create_submenu', menu_id=menu.id)
        response = await ac.post(req_url, follow_redirects=True,
                                 json={
                                     'title': 'title1',
                                     'description': 'description1'
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

        # Create dishes
        for num in range(1, 3):
            req_url = api.url_path_for('create_dish', menu_id=menu.id, submenu_id=submenu.id)
            response = await ac.post(req_url, follow_redirects=True,
                                     json={
                                         'title': f'title{num}',
                                         'description': f'description{num}',
                                         'price': f'54.1{num}'
                                     })
            assert response.status_code == 201, 'Can`t create dish'
            assert response.json()['title'], 'Response haven`t a field title'
            assert response.json()['id'], 'Response haven`t a field id'
            assert response.json()['description'], 'Response haven`t a field description'
            assert response.json()['price'], 'Response haven`t a field price'
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

        # Watch menu
        req_url = api.url_path_for('get_menu', menu_id=menu.id)
        response = await ac.get(req_url, follow_redirects=True)
        assert response.status_code == 200, 'Can`t get menu by id'
        assert str(menu.id) == response.json()['id'], 'Menu id is not equal'
        assert menu.title == response.json()['title'], 'Menu title is not equal'
        assert menu.description == response.json()['description'], 'Menu description is not equal'
        assert response.json()['submenus_count'] == 1, 'Invalid submenus count'
        assert response.json()['dishes_count'] == 2, 'Invalid dishes count'

        # Watch submenu
        req_url = api.url_path_for('get_submenu', menu_id=1, submenu_id=submenu.id)
        response = await ac.get(req_url, follow_redirects=True)
        assert response.status_code == 200, 'Can`t get submenu by id'
        assert str(submenu.id) == response.json()['id'], 'Submenu id is not equal'
        assert submenu.title == response.json()['title'], 'Submenu title is not equal'
        assert submenu.description == response.json()['description'], 'Submenu description is not equal'
        assert response.json()['dishes_count'] == 2, 'Invalid dishes count'

        # Delete submenu
        req_url = api.url_path_for('delete_submenu', menu_id=menu.id, submenu_id=submenu.id)
        response = await ac.delete(req_url, follow_redirects=True)
        assert response.status_code == 200, 'Can`t delete submenu by id'
        assert not response.json(), 'Invalid response'

        # Watch submenus
        req_url = api.url_path_for('get_all_submenus_in_menu', menu_id=menu.id)
        response = await ac.get(req_url, follow_redirects=True)
        assert response.status_code == 200, 'Can`t get all submenus'
        assert response.text[0] == '[' and response.text[-1] == ']', 'Response json is not a list'

        # Watch dishes
        req_url = api.url_path_for('get_all_dishes_in_submenu', menu_id=menu.id, submenu_id=submenu.id)
        response = await ac.get(req_url, follow_redirects=True)
        assert response.status_code == 200, 'Can`t get all dishes'
        assert response.text[0] == '[' and response.text[-1] == ']', 'Response json is not a list'

        # Watch menu
        req_url = api.url_path_for('get_menu', menu_id=menu.id)
        response = await ac.get(req_url, follow_redirects=True)
        assert response.status_code == 200, 'Can`t get menu by id'
        assert str(menu.id) == response.json()['id'], 'Menu id is not equal'
        assert menu.title == response.json()['title'], 'Menu title is not equal'
        assert menu.description == response.json()['description'], 'Menu description is not equal'
        assert response.json()['submenus_count'] == 0, 'Invalid submenus count'
        assert response.json()['dishes_count'] == 0, 'Invalid dishes count'

        # Delete menu
        req_url = api.url_path_for('delete_menu', menu_id=menu.id)
        response = await ac.delete(req_url, follow_redirects=True)
        assert response.status_code == 200, 'Can`t delete menu by id'
        assert not response.json(), 'Invalid response'

        # Show menus
        req_url = api.url_path_for('get_all_menus')
        response = await ac.get(req_url, follow_redirects=True)
        assert response.status_code == 200, 'Can`t get all menus'
        assert response.text[0] == '[' and response.text[-1] == ']', 'Response json is not a list'
