# Restaurant API
_________________
## Info

The excel file for data extraction is located at the [link](https://docs.google.com/spreadsheets/d/1g73VTQrxzM5YCn2kw4Cc4BrjJ_vQ_qCgErDgSMJAg_8). The file is open to everyone for editing.

## How to run
Clone the repository from Github and go to project directory:
```
git clone https://github.com/klishchov-bohdan/restaurant-api
cd ./restaurant-api
```
Rename the file `.env.prod.dist` to `.env.prod` and fill in the environment variables as follows (already filled):
```
POSTGRES_HOST = db
POSTGRES_PORT = 1221
POSTGRES_USER = postgres
POSTGRES_PASSWORD = pass
POSTGRES_DB = postgres

TEST_POSTGRES_HOST = db_test
TEST_POSTGRES_PORT = 1222
TEST_POSTGRES_USER = postgres
TEST_POSTGRES_PASSWORD = pass
TEST_POSTGRES_DB = postgres

REDIS_SERVER = cache-redis
REDIS_PORT = 6379

RABBITMQ_DEFAULT_USER = rmuser
RABBITMQ_DEFAULT_PASSWORD = rmpassword
RABBITMQ_PORT_WEB = 15672
RABBITMQ_PORT = 5672
RABBITMQ_HOST = rabbitmq
```
Using the google console, create a project and a service account, download its credentials in json format and place it in the project folder. The file should be called `credentials.json`

Create a new Docker network using the command:

```
docker network create "my-net"
```
Run the following command to deploy the restaurant API and databases:
```
docker compose --env-file .env.prod up --build cache-redis rabbitmq celery flower db app
```
or with `make` command (must be installed make):

```
make run_docker
```

After which `docker сompose` will create three containers with a databases and a Python application and install all dependencies. You can access the API documentation by url address `http://localhost:8000/docs`


### Flower
You can access the Celery worker processes through the Flower app by url `http://localhost:8888`

### RabbitMQ
You can access to RabbitMQ by url `http://localhost:15672`

## Completed additional tasks
Task  | Location
------------- | -------------
Обновление меню из google sheets раз в 15 сек. | [File](https://github.com/klishchov-bohdan/restaurant-api/blob/master/app/background/tasks.py)
Блюда по акции. Размер скидки (%) указывается в столбце G файла Menu.xlsx |  [File](https://github.com/klishchov-bohdan/restaurant-api/blob/master/app/schemas.py)

Cache invalidation loads in background task in this [file](https://github.com/klishchov-bohdan/restaurant-api/blob/master/app/dependencies.py)
## Tests
To pass testing you just need to run the test container using the following command (API and databases should be deployed with previous command):
```
docker compose --env-file .env.prod up --build cache-redis rabbitmq db_test app_tests
```
or
```
make run_docker_tests
```
After tests passed container finish to work automatically
