# Makefile for DevPrepLab

.PHONY: help install clean \
	backend-install backend-run backend-db-migrate backend-test backend-create-test-db \
	frontend-install frontend-run frontend-build frontend-lint \
	docker-up docker-down docker-build backend-up frontend-up db-up

help:
	@echo "Makefile for DevPrepLab"
	@echo ""
	@echo "Usage:"
	@echo "  make help                      Show this help message"
	@echo "  make install                   Install all dependencies for backend and frontend"
	@echo "  make clean                     Remove generated files"
	@echo ""
	@echo "Backend:"
	@echo "  make backend-install           Install backend dependencies"
	@echo "  make backend-run               Run the backend server"
	@echo "  make backend-db-migrate        Run database migrations"
	@echo "  make backend-test              Run backend tests"
	@echo "  make backend-create-test-db    Ensure test database exists"
	@echo ""
	@echo "Frontend:"
	@echo "  make frontend-install          Install frontend dependencies"
	@echo "  make frontend-run              Run the frontend dev server"
	@echo "  make frontend-build            Build the frontend application"
	@echo "  make frontend-lint             Lint the frontend code"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up                 Start all services with Docker Compose"
	@echo "  make backend-up                Start only the backend service with Docker Compose"
	@echo "  make frontend-up               Start only the frontend service with Docker Compose"
	@echo "  make db-up                     Start only the database service with Docker Compose"
	@echo "  make docker-down               Stop the application with Docker Compose"
	@echo "  make docker-build              Build the Docker images"

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
# Backend Commands (delegating to backend/Makefile)
# ==============================================================================

backend-install:
	@echo ">>> Installing backend dependencies..."
	@$(MAKE) -C backend install

backend-create-test-db:
	@echo ">>> Ensuring test database exists..."
	@$(MAKE) -C backend create-test-db

backend-test:
	@echo ">>> Running backend tests..."
	@$(MAKE) -C backend test

backend-run:
	@echo ">>> Starting backend server..."
	@$(MAKE) -C backend run

backend-db-migrate:
	@echo ">>> Running database migrations..."
	@$(MAKE) -C backend db-migrate

# ==============================================================================
# Frontend Commands (delegating to frontend/Makefile)
# ==============================================================================

frontend-install:
	@echo ">>> Installing frontend dependencies..."
	@$(MAKE) -C frontend install

frontend-run:
	@echo ">>> Starting frontend dev server..."
	@$(MAKE) -C frontend dev

frontend-build:
	@echo ">>> Building frontend application..."
	@$(MAKE) -C frontend build

frontend-lint:
	@echo ">>> Linting frontend code..."
	@$(MAKE) -C frontend lint

# ==============================================================================
# Docker Commands
# ==============================================================================

docker-up: ## Start all services in detached mode
	@echo ">>> Starting all services with Docker Compose..."
	@docker-compose up -d

.PHONY: backend-up
backend-up: ## Start only the backend service in detached mode
	docker-compose up -d backend

.PHONY: frontend-up
frontend-up: ## Start only the frontend service in detached mode
	docker-compose up -d frontend

.PHONY: db-up
db-up: ## Start only the database service in detached mode
	docker-compose up -d postgres

docker-down:
	@echo ">>> Stopping application with Docker Compose..."
	@docker-compose down

docker-build:
	@echo ">>> Building Docker images..."
	@docker-compose build
