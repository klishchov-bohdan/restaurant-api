#!/bin/bash


pytest -v ./tests/test_count.py
pytest -v ./tests/test_menu.py ./tests/test_submenu.py ./tests/test_dish.py
#rm .env
#cp ./.env.test ./.env
#alembic upgrade head
#gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000