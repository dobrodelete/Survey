import sqlite3

from config import DB_NAME, ADMIN_NAME, ADMIN_PASSWORD


def setup_project():
    try:
        with open("misc/create.sql", "r") as file:
            sql_db_setup = file.read()
        sqlite_connection = sqlite3.connect(DB_NAME)
        sql_create_admin = f"INSERT INTO admins (name, password) VALUES (?, ?);"
        cursor = sqlite_connection.cursor()
        cursor.executescript(sql_db_setup)
        sqlite_connection.commit()
        admin = (ADMIN_NAME, ADMIN_PASSWORD)
        cursor.execute(sql_create_admin, admin)
        sqlite_connection.commit()
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    setup_project()
