import os
from pathlib import Path

import psycopg2

from app.config import settings


MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"


def run_migrations():
    if not settings.db_password:
        raise RuntimeError(
            "MYGEMS_DB_PASSWORD is not set. Copy .env.example to .env and fill the password."
        )

    conn = psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
    )
    conn.autocommit = True

    migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    for migration_file in migration_files:
        print(f"Running migration: {migration_file.name}")
        sql = migration_file.read_text(encoding="utf-8")
        with conn.cursor() as cur:
            cur.execute(sql)

    conn.close()
    print(f"Applied {len(migration_files)} migrations to {settings.db_name}.")


if __name__ == "__main__":
    run_migrations()
