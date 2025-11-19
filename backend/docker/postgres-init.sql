-- Initialization script for PostgreSQL in Docker
-- This script runs only on first container startup when the data directory is empty.
-- It creates the test database used by automated tests.

CREATE DATABASE test_devpreplab;
