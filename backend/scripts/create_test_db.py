"""Utility to ensure the test database exists.

Usage (from repo root):

    cd backend
    python -m scripts.create_test_db

It reads database connection details from app.core.config.settings
and creates the test database (settings.POSTGRES_DB_TEST) if needed.
"""

import sys

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errors import DuplicateDatabase

from app.core.config import settings


def ensure_test_db() -> None:
    db_name = settings.POSTGRES_DB_TEST
    host = settings.POSTGRES_SERVER
    port = settings.POSTGRES_PORT
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD

    print(
        f"Ensuring test database exists:\n"
        f"  host={host} port={port} user={user} db={db_name}"
    )

    # Connect to the maintenance database (usually 'postgres')
    conn = connect(
        dbname="postgres",
        user=user,
        password=password,
        host=host,
        port=port,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    try:
        with conn.cursor() as cur:
            # Check if database already exists
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            exists = cur.fetchone() is not None

            if exists:
                print(f"Database '{db_name}' already exists; nothing to do.")
                return

            print(f"Creating database '{db_name}'...")
            try:
                cur.execute(f"CREATE DATABASE {db_name};")
            except DuplicateDatabase:
                # In case of race conditions
                print(f"Database '{db_name}' was created concurrently; ignoring.")
            else:
                print(f"Database '{db_name}' created successfully.")
    finally:
        conn.close()


def main() -> int:
    try:
        ensure_test_db()
    except Exception as exc:  # pragma: no cover - simple CLI wrapper
        print(f"Error while ensuring test database exists: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
