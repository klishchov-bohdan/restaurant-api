from httpx import AsyncClient


class TestSubmenu:
    async def test_get_all_submenus(self, ac: AsyncClient):
        response = await ac.get('/menus/1/submenus', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get all submenus'
        assert response.text[0] == '[' and response.text[-1] == ']', 'Response json is not a list'

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

    async def test_get_menu(self, ac: AsyncClient):
        response = await ac.get('/menus/1/submenus/2', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get submenu by id'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['id'] == '2', 'Invalid submenu response'

    async def test_update(self, ac: AsyncClient):
        response = await ac.patch('/menus/1/submenus/2', follow_redirects=True,
                                  json={
                                      'title': 'new_title',
                                      'description': 'new_description'
                                  })
        assert response.status_code == 200, 'Can`t update submenu'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['id'] == '2', 'Invalid submenu id response'
        assert response.json()['title'] == 'new_title', 'Invalid submenu title response'
        assert response.json()['description'] == 'new_description', 'Invalid submenu description response'

    async def test_delete(self, ac: AsyncClient):
        response = await ac.delete('/menus/1/submenus/2', follow_redirects=True)
        assert response.status_code == 200, 'Can`t delete submenu by id'
        assert not response.json(), 'Invalid response'
