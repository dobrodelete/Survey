import sqlite3
import os

from config import DB_NAME, ADMIN_NAME, ADMIN_PASSWORD, MAIN_REPORTS_FOLDER, JSON_REPORTS_FOLDER, XLSX_REPORTS_FOLDER


def setup_project():
    try:
        # setup db
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

        # setup dirs
        os.mkdir(MAIN_REPORTS_FOLDER)
        os.mkdir(f"{MAIN_REPORTS_FOLDER}/{XLSX_REPORTS_FOLDER}")
        os.mkdir(f"{MAIN_REPORTS_FOLDER}/{JSON_REPORTS_FOLDER}")

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    setup_project()
