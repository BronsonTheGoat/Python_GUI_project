from PyQt6.QtWidgets import QApplication, QDialog, QFormLayout
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from sqlconnector import create_connection

class EditBookDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        # if create_connection("QSQLITE", "library"):
        #     print("Connected succesfully.")
        #     self.db = QSqlDatabase.database()
        #     if not self.db.isOpen():
        #         print("Database is not open!")
        # else:
        #     print("Connection failed")

if __name__ == "__main__":
    app = QApplication([])
    dialog = EditBookDialog()
    dialog.exec()
    app.exec()