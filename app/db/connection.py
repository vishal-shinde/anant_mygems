import psycopg2

from app.config import settings


def get_connection():
    if not settings.db_password:
        raise RuntimeError(
            "MYGEMS_DB_PASSWORD is not set. Copy .env.example to .env and fill the real password."
        )

    return psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
    )
