.PHONY: migrate up down

up:
	poetry run python -m backend

makemigrations:
	poetry run python -m alembic revision -m "$(message)"

migrate:
	poetry run python -m alembic upgrade head

docker-up:
	docker build -t echoes-backend .
	docker run -p 8000:8000 -it echoes-backend
