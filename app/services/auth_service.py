import bcrypt

from app.db.connection import get_connection


def authenticate(username: str, password: str):
    if not username or not password:
        return None

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT user_id, username, password_hash, role_id, is_active
                FROM users
                WHERE username = %s
                LIMIT 1
                """,
                (username,),
            )
            row = cur.fetchone()

    if row is None:
        return None

    user_id, db_username, password_hash, role_id, is_active = row
    if not is_active:
        return None

    if not bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
        return None

    return {
        "user_id": user_id,
        "username": db_username,
        "role_id": role_id,
    }
