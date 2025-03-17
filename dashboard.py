from PyQt6.QtWidgets import QApplication, QDialog, QFormLayout, QMessageBox
from db_handler import DatabaseHandler
import os
import sys

class DashboardDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

if __name__ == "__main__":
    app = QApplication([])
    if not DatabaseHandler():
        QMessageBox.critical("Error", "Databasse is not available!")
        sys.exit(1)
    else:
        conn = DatabaseHandler()
    dialog = DashboardDialog()
    dialog.exec()
    app.exec()