"""
This mdule is contains the sql connector function.
"""
from PyQt6.QtSql import QSqlDatabase
import os
import sys

script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

def create_connection(driver: str, database: str) -> bool:
    """
    This function creates an SQL connection with the given QSql driver
    
    Returns:
       bool: Returns True if the database connection is opened successfully else returns False.
    """
    db = QSqlDatabase.addDatabase(driver)
    db.setDatabaseName(f"{script_directory}/{database}.db")

    if not db.open():
        print("Unable to establish a database connection.")
        return False

    return True

if __name__ == "__main__":
    pass