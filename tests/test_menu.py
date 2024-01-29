from httpx import AsyncClient


class TestMenu:
    async def test_get_all_menus(self, ac: AsyncClient):
        response = await ac.get('/menus', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get all menus'
        assert response.text[0] == '[' and response.text[-1] == ']', 'Response json is not a list'

    async def test_create(self, ac: AsyncClient):
        response = await ac.post('/menus', follow_redirects=True,
                                 json={
                                     "title": "title1",
                                     "description": "description1"
                                 })
        assert response.status_code == 201, 'Can`t create menu'
        assert response.json()['title'], 'Response haven`t a field title'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['description'], 'Response haven`t a field description'

    async def test_get_menu(self, ac: AsyncClient):
        response = await ac.get('/menus/2', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get menu by id'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['id'] == '2', 'Invalid menu response'

    async def test_update(self, ac: AsyncClient):
        response = await ac.patch('/menus/2', follow_redirects=True,
                                  json={
                                      'title': 'new_title',
                                      'description': 'new_description'
                                  })
        assert response.status_code == 200, 'Can`t update menu'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['id'] == '2', 'Invalid menu id response'
        assert response.json()['title'] == 'new_title', 'Invalid menu title response'
        assert response.json()['description'] == 'new_description', 'Invalid menu description response'

    async def test_delete(self, ac: AsyncClient):
        response = await ac.delete('/menus/2', follow_redirects=True)
        assert response.status_code == 200, 'Can`t delete menu by id'
        assert not response.json(), 'Invalid response'

