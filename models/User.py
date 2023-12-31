import sqlite3

from config import DB_NAME


class User:
    def __init__(self):
        db = sqlite3.connect(f"C:\Edu\Survey\{DB_NAME}")
        try:
            db.execute('CREATE TABLE admins(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, password TEXT NOT NULL)')
        except:
            pass
        try:
            db.execute('INSERT INTO admins (name, password) VALUES (?, ?)', ('admin', 'admin'))
        except:
            pass

    def check_auth(self, login: str, passw: str) -> bool:
        db = sqlite3.connect(f"{DB_NAME}")
        cursor = db.execute("SELECT * FROM admins;")
        for id, name, password in cursor.fetchall():
            # print(id, name, password)
            if name == login and password == passw:
                # print(name, login, password, passw)
                return True
        return False
