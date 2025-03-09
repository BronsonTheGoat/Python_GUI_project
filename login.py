from PyQt6.QtWidgets import QApplication, QDialog, QFormLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton
from PyQt6.QtGui import QRegularExpressionValidator, QCursor, QPalette, QColor, QPixmap, QIcon
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import os
import sys
from sqlconnector import create_connection

class LoginDialog(QDialog):
    settings_saved = pyqtSignal(dict)
    
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        if create_connection("QSQLITE", "library"):
            print("Connected succesfully.")
            self.db = QSqlDatabase.database()
            if not self.db.isOpen():
                print("Database is not open!")
        else:
            print("Connection failed")
        
        self.hide_icon = QPixmap(f"{self.script_directory}/assets/hidden.png")
        self.show_icon = QPixmap(f"{self.script_directory}/assets/eye.png")

        self.setWindowTitle("Login")

        self.layout = QFormLayout(self)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.show_password_button = QPushButton(self)
        self.show_password_button.setIcon(QIcon(self.show_icon))
        self.show_password_button.clicked.connect(self.show_password)
        
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.show_password_button)

        self.layout.addRow(self.username_input)
        self.layout.addRow(self.password_input, self.show_password_button)

        login_button = QPushButton("Login", self)
        login_button.clicked.connect(self.login_user)
        self.layout.addWidget(login_button)

    # Methods
    def login_user(self):
        print("Query from database...")
        query = QSqlQuery(self.db)
        query.prepare("SELECT * FROM users WHERE username = ? AND password = ?")
        query.addBindValue(f'{self.username_input.text()}')
        query.addBindValue(f'{self.password_input.text()}')
        users = []

        if query.exec():
            while query.next():
                print(query.value(1))
                user_id = query.value(0)
                name = query.value(1)
                users.append((user_id, name))
        else:
            print("Error fetching users:", query.lastError().text())

        print(users)
        return users
        
    def show_password(self) -> None:
        if self.password_input.echoMode() == QLineEdit.EchoMode.Normal:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_password_button.setIcon(QIcon(self.show_icon))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_password_button.setIcon(QIcon(self.hide_icon))


if __name__ == "__main__":
    app = QApplication([])
    dialog = LoginDialog()
    dialog.exec()
    app.exec()