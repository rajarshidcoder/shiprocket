.PHONY: help build up down logs shell migrate test lint format clean

help:
	@echo "Available commands:"
	@echo "  make build      - Build Docker containers"
	@echo "  make up         - Start all services"
	@echo "  make down       - Stop all services"
	@echo "  make logs       - View logs"
	@echo "  make shell      - Open shell in backend container"
	@echo "  make migrate    - Run database migrations"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linters"
	@echo "  make format     - Format code"
	@echo "  make clean      - Clean up containers and volumes"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec backend /bin/bash

migrate:
	docker-compose exec backend alembic upgrade head

migrate-create:
	docker-compose exec backend alembic revision --autogenerate -m "$(msg)"

test:
	docker-compose exec backend pytest

lint:
	docker-compose exec backend flake8 app
	docker-compose exec backend mypy app

format:
	docker-compose exec backend black app
	docker-compose exec backend isort app

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
