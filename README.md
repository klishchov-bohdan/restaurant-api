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
Run the following commands to deploy the restaurant API:
```
docker compose build
docker compose up
```
After which `docker сompose` will create two containers with a database and a Python application and install all dependencies. You can access the API documentation by url address `http://localhost:8000/docs`
