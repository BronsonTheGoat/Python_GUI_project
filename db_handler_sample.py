import sqlite3

class DatabaseHandler:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        """Kapcsolódás az adatbázishoz"""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def close(self):
        """Kapcsolat lezárása"""
        self.connection.commit()
        self.connection.close()

    def execute_query(self, query, params=None):
        """Kérés futtatása az adatbázisban"""
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute_non_query(self, query, params=None):
        """Kérés futtatása adatbázis módosításhoz"""
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        self.connection.commit()
