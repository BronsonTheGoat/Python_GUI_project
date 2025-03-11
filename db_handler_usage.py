from PyQt6.QtWidgets import QWidget
from db_handler_sample import DatabaseHandler

class MyForm(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseHandler('mydatabase.db')
        self.db.connect()

        # Itt az adatbázis hívások, pl. bejelentkezés, regisztráció

    def register_user(self, username, password):
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        self.db.execute_non_query(query, (username, password))

    def get_user(self, username):
        query = "SELECT * FROM users WHERE username = ?"
        return self.db.execute_query(query, (username,))

    def closeEvent(self, event):
        self.db.close()  # Bezárjuk az adatbázis kapcsolatot
        event.accept()
