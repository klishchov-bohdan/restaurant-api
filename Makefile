start:
	alembic upgrade head && gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
start_dev:
	uvicorn app.main:app --reload
tests_crud:
	pytest -v ./tests/test_menu.py ./tests/test_submenu.py ./tests/test_dish.py
tests_count:
	pytest -v ./tests/test_count.py