# Backend Makefile for DevPrepLab

VENV_PREFIX = . .venv/bin/activate &&

.PHONY: help install run test create-test-db seed-problems db-migrate db-revision db-downgrade build-execution-image clean-db

help:
	@echo "Backend Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make help                   Show this help message"
	@echo "  make install                Install backend dependencies"
	@echo "  make run                    Run the backend server"
	@echo "  make test                   Run backend tests"
	@echo "  make create-test-db         Ensure test database exists"
	@echo "  make seed-problems         Seed the database with initial problems"
	@echo "  make clean-db               Clean the database"
	@echo "  make db-migrate             Apply database migrations (alembic upgrade head)"
	@echo "  make db-revision message=\"...\"  Create a new Alembic revision"
	@echo "  make db-downgrade           Downgrade one migration (alembic downgrade -1)"
	@echo "  make build-execution-image  Build the Docker code-execution image"

install:
	$(VENV_PREFIX) pip install -r requirements.txt

run:
	$(VENV_PREFIX) uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	$(VENV_PREFIX) pytest

create-test-db:
	$(VENV_PREFIX) python -m scripts.create_test_db

seed-problems: db-migrate
	$(VENV_PREFIX) python -m scripts.seed_problems

clean-db:
	$(VENV_PREFIX) python -m scripts.clean_db
	$(MAKE) db-migrate

db-migrate:
	$(VENV_PREFIX) alembic upgrade head
db-revision:
	$(VENV_PREFIX) alembic revision --autogenerate -m "$$message"

db-downgrade:
	$(VENV_PREFIX) alembic downgrade -1

build-execution-image:
	docker build -t devpreplab-execution:latest -f docker/execution/Dockerfile .
