.PHONY: migrate up down

up:
	poetry run python -m backend

makemigrations:
	alembic revision --autogenerate -m "$(message)"

migrate:
	poetry run python -m alembic upgrade head
