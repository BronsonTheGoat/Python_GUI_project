import sqlite3
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMessageBox

class DatabaseHandler:
    def __init__(self, driver, db_name):
        self.db_name = db_name

    def connect(self):
        """Kapcsolódás az adatbázishoz"""
        db = QSqlDatabase.addDatabase(self.driver)
        db.setDatabaseName(self.db_name)

        if not db.open():
            QMessageBox.critical(None, "Database Error", db.lastError().text())
            return False
        return True

    def execute_query(self, sql_query, params=None):
        """Kérés futtatása az adatbázisban"""
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        # return self.cursor.fetchall()
    
        query = QSqlQuery()
        query.prepare(sql_query)
        for item in params:
            query.addBindValue(params)
        records = []

        if query.exec():
            while query.next():
                customer_id = query.value(0)
                name = query.value(1)
                age = query.value(2)
                records.append((customer_id, name, age))
        else:
            print("Error fetching customers:", query.lastError().text())

        return records

    def execute_non_query(self, query, params=None):
        """Kérés futtatása adatbázis módosításhoz"""
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        self.connection.commit()
