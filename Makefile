start:
	alembic upgrade head && gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
start_dev:
	uvicorn app.main:app --reload
run_docker:
	docker compose --env-file .env.prod up --build cache-redis rabbitmq celery flower db app
run_docker_tests:
	docker compose --env-file .env.prod up --build cache-redis rabbitmq db_test app_tests
tests_crud:
	pytest -v ./tests/test_menu.py ./tests/test_submenu.py ./tests/test_dish.py
tests_count:
	pytest -v ./tests/test_count.py
