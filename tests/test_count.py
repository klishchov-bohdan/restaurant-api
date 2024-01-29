from httpx import AsyncClient


class TestDishesAndSubmenusCount:
    menu_submenus_count = 1
    menu_dishes_count = 3
    submenu_dishes_count = 3

    async def test_create_dishes(self, ac: AsyncClient):
        for num in range(1, self.submenu_dishes_count + 1):
            response = await ac.post('/menus/1/submenus/1/dishes', follow_redirects=True,
                                     json={
                                         "title": f"title{num}",
                                         "description": f"description{num}",
                                         "price": f"54.1{num}"
                                     })
            assert response.status_code == 201, 'Can`t create dish'
            assert response.json()['title'], 'Response haven`t a field title'
            assert response.json()['id'], 'Response haven`t a field id'
            assert response.json()['description'], 'Response haven`t a field description'
            assert response.json()['price'], 'Response haven`t a field price'

    async def test_menu_count_check(self, ac: AsyncClient):
        response = await ac.get(f'/menus/1', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get menu by id'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['id'] == '1', 'Invalid menu response'
        assert response.json()['submenus_count'] == self.menu_submenus_count, 'Invalid submenus count in menu'
        assert response.json()['dishes_count'] == self.menu_dishes_count, 'Invalid dishes count in menu'

    async def test_submenu_count_check(self, ac: AsyncClient):
        response = await ac.get(f'/menus/1/submenus/1', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get menu by id'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['id'] == '1', 'Invalid menu response'
        assert response.json()['dishes_count'] == self.submenu_dishes_count, 'Invalid dishes count in submenu'

    async def test_delete_submenu(self, ac: AsyncClient):
        response = await ac.delete('/menus/1/submenus/1', follow_redirects=True)
        assert response.status_code == 200, 'Can`t delete submenu by id'
        assert not response.json(), 'Invalid response'

    async def test_get_all_submenus(self, ac: AsyncClient):
        response = await ac.get('/menus/1/submenus', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get all submenus'
        assert response.text == '[]', 'Response is not empty list'

    async def test_get_all_dishes(self, ac: AsyncClient):
        response = await ac.get('/menus/1/submenus/1/dishes', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get all dishes'
        assert response.text == '[]', 'Response is not empty list'

    async def test_get_menu(self, ac: AsyncClient):
        response = await ac.get('/menus/1', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get menu by id'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['id'] == '1', 'Invalid menu response'
        assert response.json()['submenus_count'] == 0, 'Invalid submenus count in menu'
        assert response.json()['dishes_count'] == 0, 'Invalid dishes count in menu'

    async def test_delete_menu(self, ac: AsyncClient):
        response = await ac.delete('/menus/1', follow_redirects=True)
        assert response.status_code == 200, 'Can`t delete menu by id'
        assert not response.json(), 'Invalid response'

    async def test_get_all_menus(self, ac: AsyncClient):
        response = await ac.get('/menus', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get all menus'
        assert response.text == '[]', 'Response is not empty list'
