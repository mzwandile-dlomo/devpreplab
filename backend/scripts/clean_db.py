
import sys
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.core.config import settings

def clean_databases():
    databases_to_drop = [settings.POSTGRES_DB, settings.POSTGRES_DB_TEST]
    
    conn = connect(
        dbname="postgres",
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_SERVER,
        port=settings.POSTGRES_PORT,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    with conn.cursor() as cur:
        for db_name in databases_to_drop:
            # Terminate all connections to the database
            cur.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{db_name}'
              AND pid <> pg_backend_pid();
            """)
            
            print(f"Dropping database '{db_name}'...")
            cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
            print(f"Database '{db_name}' dropped.")
            
            print(f"Creating database '{db_name}'...")
            cur.execute(f"CREATE DATABASE {db_name};")
            print(f"Database '{db_name}' created.")

    conn.close()

if __name__ == "__main__":
    try:
        clean_databases()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)
