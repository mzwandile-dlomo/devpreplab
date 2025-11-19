# Makefile for DevPrepLab

.PHONY: help install clean backend-install backend-run backend-db-migrate frontend-install frontend-run frontend-build frontend-lint docker-up docker-down docker-build

help:
	@echo "Makefile for DevPrepLab"
	@echo ""
	@echo "Usage:"
	@echo "  make help                  Show this help message"
	@echo "  make install               Install all dependencies for backend and frontend"
	@echo "  make clean                 Remove generated files"
	@echo ""
	@echo "Backend:"
	@echo "  make backend-install       Install backend dependencies"
	@echo "  make backend-run           Run the backend server"
	@echo "  make backend-db-migrate    Run database migrations"
	@echo ""
	@echo "Frontend:"
	@echo "  make frontend-install      Install frontend dependencies"
	@echo "  make frontend-run          Run the frontend dev server"
	@echo "  make frontend-build        Build the frontend application"
	@echo "  make frontend-lint         Lint the frontend code"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up             Start all services with Docker Compose"
	@echo "  make backend-up            Start only the backend service with Docker Compose"
	@echo "  make frontend-up           Start only the frontend service with Docker Compose"
	@echo "  make docker-down           Stop the application with Docker Compose"
	@echo "  make docker-build          Build the Docker images"

# ==============================================================================
# General Commands
# ==============================================================================

install: backend-install frontend-install

clean:
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -rf frontend/.next
	@rm -rf frontend/node_modules

# ==============================================================================
# Backend Commands
# ==============================================================================

backend-install:
	@echo ">>> Installing backend dependencies..."
	@pip install -r backend/requirements.txt

backend-test:
	@echo ">>> Running backend tests..."
	@cd backend && python -m pytest

backend-run:
	@echo ">>> Starting backend server..."
	@uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --app-dir backend/app

backend-db-migrate:
	@echo ">>> Running database migrations..."
	@alembic -c backend/alembic.ini upgrade head

# ==============================================================================
# Frontend Commands
# ==============================================================================

frontend-install:
	@echo ">>> Installing frontend dependencies..."
	@npm install --prefix frontend

frontend-run:
	@echo ">>> Starting frontend dev server..."
	@npm run dev --prefix frontend

frontend-build:
	@echo ">>> Building frontend application..."
	@npm run build --prefix frontend

frontend-lint:
	@echo ">>> Linting frontend code..."
	@npm run lint --prefix frontend

# ==============================================================================
# Docker Commands
# ==============================================================================

up: ## Start all services in detached mode
	docker-compose up -d

.PHONY: backend-up
backend-up: ## Start only the backend service in detached mode
	docker-compose up -d backend

.PHONY: frontend-up
frontend-up: ## Start only the frontend service in detached mode
	docker-compose up -d frontend

docker-down:
	@echo ">>> Stopping application with Docker Compose..."
	@docker-compose down

docker-build:
	@echo ">>> Building Docker images..."
	@docker-compose build
