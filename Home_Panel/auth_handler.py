from database.database import get_connection


def authenticate(username, password):

    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "123"

    if (
        username == ADMIN_USERNAME
        and password == ADMIN_PASSWORD
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO login_activity (username)
        VALUES (?)
        """, (username,))

        conn.commit()
        conn.close()

        return True

    return False