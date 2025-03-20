from PyQt6.QtWidgets import QApplication, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QMessageBox, QComboBox,\
    QPushButton, QAbstractScrollArea
from PyQt6.QtGui import  QIcon
from PyQt6.QtCore import QSize
from db_handler import DatabaseHandler
import os
import sys

class DashboardDialog(QDialog):
    def __init__(self, conn, session, parent=None) -> None:
        super().__init__(parent)
        
        self.script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.db = conn
        
        self.session = session
        
        self.setWindowTitle("Library app")
        self.setFixedSize(QSize(900, 300))
        self.setWindowIcon(QIcon(f"{self.script_directory}/assets/dashboard.png"))
        
        self.main_layout = QVBoxLayout()
        self.users_table = QTableWidget()
        # self.users_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.users_table.horizontalHeader().setStretchLastSection(False )
        
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.users_table)
        
        self.get_users()
        self.fill_table()
    
    def fill_table(self):        
        self.users_table.setRowCount(len(self.users))
        self.users_table.setColumnCount(len(self.headers)) # for delete button
        self.users_table.setHorizontalHeaderLabels(self.headers)
        
        for row, column in enumerate(self.users):
            authority_box = QComboBox()
            authority_box.addItems(("superadmin", "admin", "user"))
            for col in range(self.users_table.columnCount()):
                if col < 7:
                    self.users_table.setItem(row, col, QTableWidgetItem(str(column[col])))
                elif col == 7:
                    authority_box.setCurrentText(column[col])
                    authority_box.currentTextChanged.connect(self.authority_changed)
                    self.users_table.setCellWidget(row,col, authority_box)
                else:
                    delete_user_btn = QPushButton("Delete user")
                    delete_user_btn.clicked.connect(self.delete_user)
                    self.users_table.setCellWidget(row, col, delete_user_btn)
                    
                    
                
        # TODO: for the last column add a dropdown with 3 options: superadmin, admin, user
        # TODO: add extra column with delete user button 
                
        self.users_table.cellChanged.connect(self.cell_changed)
        
    def get_users(self):
        self.headers = [item[1] for item in self.db.fetch("PRAGMA table_info (users)")]
        self.headers.append("Delete user")
        self.users = self.db.fetch("SELECT * FROM users")
    
    def cell_changed(self, row, col):
        if self.users_table.item(row, col).text() != self.users[row][col]:
            buttons = QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Apply
            response = QMessageBox.warning(self, "User data changed", f"You changed the user data in row {row}!\nWould you like to save the changes?", buttons)
            if response == QMessageBox.StandardButton.Apply:
                self.users[row][col] = self.users_table.item(row, col).text()
                self.update_user_data(row, col)
            else:
                self.users_table.item(row, col).setText(self.users[row][col])
                
    def authority_changed(self, text):
        index = self.users_table.indexAt(self.sender().pos())
        if text != self.users[index.row()][index.column()]:
            buttons = QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Apply
            response = QMessageBox.warning(self, "User data changed", f"You changed the user data in row {index.row()}!\nWould you like to save the changes?", buttons)
            if response == QMessageBox.StandardButton.Apply:
                self.users[index.row()][index.column()] = text
                self.update_user_data(index.row(), index.column())
            else:
                self.sender().setCurrentText(self.users[index.row()][index.column()])
    
    def delete_user(self):
        index = self.users_table.indexAt(self.sender().pos())
        row = index.row()
        col = index.column()
        buttons = QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes
        response = QMessageBox.warning(self, "Delete user", "You are going to delete this user. Are you sure?", buttons)
        if response == QMessageBox.StandardButton.Yes:
            self.users.pop(row)
            self.delete_user_from_db(row)
        else:
            self.sender().setCurrentText(self.users[row][col])
            
    def update_user_data(self, row, col):
        params = [self.users[row][col], row + 1]
        self.db.execute_non_query(f"UPDATE users SET {self.headers[col]} = ? WHERE id = ?", params)
    
    def delete_user_from_db(self, row):
        self.db.execute_non_query(f"DELETE FROM users WHERE id = ?", row + 1)
        self.users_table.removeRow(row)

if __name__ == "__main__":
    app = QApplication([])
    if not DatabaseHandler():
        QMessageBox.critical("Error", "Databasse is not available!")
        sys.exit(1)
    else:
        conn = DatabaseHandler()
    session = {"user": "Admin",
                "auth":"superadmin",
                "started": True}
    dialog = DashboardDialog(conn, session)
    dialog.exec()
    sys.exit(1)
    app.exec()