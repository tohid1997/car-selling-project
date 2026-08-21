from app.database.connection import get_connection


def find_user_by_credentials(username, password):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username = %s
              AND password = %s
            """,
            (username, password)
        )

        return cursor.fetchone()

    finally:
        conn.close()


def create_user(username, password):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (%s, %s)
            """,
            (username, password)
        )

        conn.commit()

    finally:
        conn.close()