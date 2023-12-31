.PHONY: migrate up down

up:
	poetry run python -m backend

makemigrations:
	poetry run python -m alembic revision -m "$(message)"

migrate:
	poetry run python -m alembic upgrade head
