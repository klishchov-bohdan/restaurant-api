import re

from httpx import AsyncClient


class TestDish:
    async def test_get_all_dishes(self, ac: AsyncClient):
        response = await ac.get('/menus/1/submenus/1/dishes', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get all dishes'
        assert response.text[0] == '[' and response.text[-1] == ']', 'Response json is not a list'

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

    async def test_get_dish(self, ac: AsyncClient):
        response = await ac.get('/menus/1/submenus/1/dishes/1', follow_redirects=True)
        assert response.status_code == 200, 'Can`t get dish by id'
        assert response.json()['title'], 'Response haven`t a field title'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['description'], 'Response haven`t a field description'
        assert response.json()['price'], 'Response haven`t a field price'
        assert response.json()['id'] == '1', 'Invalid dish response'
        assert re.fullmatch(r'^\d+.\d\d$', response.json()['price'])

    async def test_update(self, ac: AsyncClient):
        response = await ac.patch('/menus/1/submenus/1/dishes/1', follow_redirects=True,
                                  json={
                                      'title': 'new_title',
                                      'description': 'new_description',
                                      'price': '12.65'
                                  })
        assert response.status_code == 200, 'Can`t update dish'
        assert response.json()['id'], 'Response haven`t a field id'
        assert response.json()['id'] == '1', 'Invalid dish id response'
        assert response.json()['title'] == 'new_title', 'Invalid dish title response'
        assert response.json()['description'] == 'new_description', 'Invalid dish description response'
        assert response.json()['price'] == '12.65', 'Invalid dish price response'

    async def test_delete(self, ac: AsyncClient):
        response = await ac.delete('/menus/1/submenus/1/dishes/1', follow_redirects=True)
        assert response.status_code == 200, 'Can`t delete dish by id'
        assert not response.json(), 'Invalid response'
