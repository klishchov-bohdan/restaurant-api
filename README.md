# Restaurant API
_________________
## How to run
Clone the repository from Github and go to project directory:
```
git clone https://github.com/klishchov-bohdan/restaurant-api
cd ./restaurant-api
```
Rename the file `.env.prod.dist` to `.env.prod` and fill in the environment variables as follows:
```
POSTGRES_HOST = db
POSTGRES_PORT = 1221
POSTGRES_USER = postgres
POSTGRES_PASSWORD = pass
POSTGRES_DB = postgres
```
Create a new Docker network using the command:

```
docker network create "my-net"
```
Run the following command to deploy the restaurant API and databases:
```
docker compose up --build db db_test app
```
After which `docker сompose` will create three containers with a databases and a Python application and install all dependencies. You can access the API documentation by url address `http://localhost:8000/docs`


## Tests
To pass testing you just need to run the test container using the following command (API and databases should be deployed with previous command):
```
docker compose up --build app_tests
```
After tests passed container finish to work automatically

## Database query
Getting a list of menus or a specific menu is done using one complex orm request, which can be seen in the app/services/menus/service.py module
-> [Go to file](https://github.com/klishchov-bohdan/restaurant-api/blob/master/app/services/menus/service.py)