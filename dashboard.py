from PyQt6.QtWidgets import QApplication, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QMessageBox
from PyQt6.QtGui import  QIcon
from PyQt6.QtCore import QSize
from db_handler import DatabaseHandler
import os
import sys

class DashboardDialog(QDialog):
    def __init__(self, conn, parent=None) -> None:
        super().__init__(parent)
        
        self.script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.db = conn
        
        self.setWindowTitle("Library app")
        self.setFixedSize(QSize(900, 300))
        self.setWindowIcon(QIcon(f"{self.script_directory}/assets/dashboard.png"))
        
        self.main_layout = QVBoxLayout()
        self.users_table = QTableWidget()
        
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.users_table)
        
        self.get_users()
        self.fill_table()
    
    def fill_table(self):        
        self.users_table.setRowCount(len(self.users))
        self.users_table.setColumnCount(len(self.users[0]))
        self.users_table.setHorizontalHeaderLabels(self.headers)
        
        for row, column in enumerate(self.users):
            for col in range(self.users_table.columnCount()):
                self.users_table.setItem(row, col, QTableWidgetItem(str(column[col])))
                
        # TODO: for the last column add a dropdown with 3 options: superadmin, admin, user
        # TODO: add extra column with delete user button 
                
        self.users_table.cellChanged.connect(self.cell_changed)
        
    def get_users(self):
        self.headers = [item[1] for item in self.db.fetch("PRAGMA table_info (users)")]
        self.users = self.db.fetch("SELECT * FROM users")
    
    def cell_changed(self, row, col):
        if self.users_table.item(row, col).text() != self.users[row][col]:
            buttons = QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Apply
            response = QMessageBox.warning(self, "User data changed", f"You changed the user data in row {row}!\nWould you like to save the changes?", buttons)
            if response == QMessageBox.StandardButton.Apply:
                self.update_user_data()
            else:
                self.users_table.item(row, col).setText(self.users[row][col])
            
    def update_user_data(self):
        raise NotImplementedError("update_user_data is not implemented yet")

if __name__ == "__main__":
    app = QApplication([])
    if not DatabaseHandler():
        QMessageBox.critical("Error", "Databasse is not available!")
        sys.exit(1)
    else:
        conn = DatabaseHandler()
    dialog = DashboardDialog(conn)
    dialog.exec()
    sys.exit(1)
    app.exec()