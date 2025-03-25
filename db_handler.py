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
    
    def get_db(self) -> QSqlDatabase:
        """
        Returns the 

        Returns:
            QSqlDatabase: _description_
        """
        return self.db
    
    def is_connected(self) -> bool:
        """
        Checks if the database is opened.

        Returns:
            bool: Returns True if the database is opened.
        """
        return self.db.isOpen()

    def fetch(self, sql_query: str, params=None) -> list[list[str|int]]:
        """
        Fetch data from the database.

        Args:
            sql_query (str): SQL query string
            params (list|tuple, optional): Parameters which will be binded. Defaults to None.

        Returns:
            list[list[str|int]]: The returned records from the databse.
        """
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
            print("Error fetching table:", query.lastError().text())
            return []

    def execute_non_query(self, sql_query: str, params=None) -> bool:
        """
        Executes Insert, Delete, Update queries.

        Args:
            sql_query (str): SQL query text.
            params (list|tuple, optional): Parameters which will be binded. Defaults to None.

        Returns:
            bool: Returns True if the qery executed succesfully.
        """
        if params is None:
            params = ()
        elif not isinstance(params ,list) or isinstance(params, tuple):
            params = [params]
            
        query = QSqlQuery(self.db)
        query.prepare(sql_query)
        for item in params:
            query.addBindValue(item)

        if query.exec():
            return True
        else:
            print("Error updating item:", query.lastError().text())
            return False
