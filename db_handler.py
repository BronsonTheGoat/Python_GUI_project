from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMessageBox
import os
import sys

class DatabaseHandler:
    _instance = None
        
    def __new__(cls) -> QSqlDatabase:
        script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        if cls._instance is None:
            cls._instance = super(DatabaseHandler, cls).__new__(cls)
            cls._instance.db = QSqlDatabase.addDatabase("QSQLITE")
            cls._instance.db.setDatabaseName(f"{script_directory}\library.db")
            cls._instance.db.open()
        return cls._instance
    
    def get_db(self):
        return self.db
    
    def is_connected(self):
        return self.db.isOpen()

    def fetch(self, sql_query: str, params=None) -> list[list[str|int]]:
        if params is None:
            params = []
        elif not isinstance(params ,list) or isinstance(params, tuple):
            params = [params]
            
        query = QSqlQuery(self.db)
        query.prepare(sql_query)
        
        # print(query.lastQuery(), params)
        
        for param in params:
            query.addBindValue(param)
            
        records: list = []

        if query.exec():
            while query.next():
                records.append([query.value(i) for i in range(query.record().count())])
            return records
        else:
            print("Error fetching customers:", query.lastError().text())
            return []

    def execute_non_query(self, sql_query, params=None) -> None:
        if params is None:
            params = ()
        elif not isinstance(params ,list) or isinstance(params, tuple):
            params = [params]
            
        query = QSqlQuery(self.db)
        query.prepare(sql_query)
        for item in params:
            query.addBindValue(item)

        if query.exec():
            print("Contact updated successfully!")
            return True
        else:
            print("Error updating contact:", query.lastError().text())
            return False
