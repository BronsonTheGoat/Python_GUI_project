from PyQt6.QtWidgets import QApplication, QDialog, QFormLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import os
import sys
import hashlib
from clikc_label import ClickableLabel
from sqlconnector import create_connection

class RegistrationDialog(QDialog):
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

        self.setWindowTitle("Registration")

        self.mian_layout = QFormLayout(self)
        
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Name")

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.show_password_button = QPushButton(self)
        self.show_password_button.setIcon(QIcon(self.show_icon))
        self.show_password_button.setAutoDefault(False)
        self.show_password_button.clicked.connect(lambda: self.show_password(self.password_input))
        
        self.password_2_input = QLineEdit(self)
        self.password_2_input.setPlaceholderText("Repeat password")
        self.password_2_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.show_password_2_button = QPushButton(self)
        self.show_password_2_button.setIcon(QIcon(self.show_icon))
        self.show_password_2_button.setAutoDefault(False)
        self.show_password_2_button.clicked.connect(lambda: self.show_password(self.password_2_input))
        
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_2_input)
        password_layout.addWidget(self.show_password_2_button)
        
        # TODO: brth date as date edit
        
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        
        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Phone")
        
        self.birth_input = QLineEdit(self)
        self.birth_input.setPlaceholderText("Birth")

        login_button = QPushButton("Create account", self)
        login_button.clicked.connect(self.create_user)
        
        label = QLabel("Already have an account??")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        to_reg_form = ClickableLabel("Login")
        to_reg_form.setAlignment(Qt.AlignmentFlag.AlignCenter)
        to_reg_form.clicked_signal.connect(self.show_register)

        self.mian_layout.addRow(self.name_input)
        self.mian_layout.addRow(self.username_input)
        self.mian_layout.addRow(self.password_input, self.show_password_button)
        self.mian_layout.addRow(self.password_2_input, self.show_password_2_button)
        self.mian_layout.addRow(self.email_input)
        self.mian_layout.addRow(self.phone_input)
        self.mian_layout.addRow(self.birth_input)
        self.mian_layout.addRow(login_button)
        self.mian_layout.addRow(label)
        self.mian_layout.addRow(to_reg_form)

    # Methods
    def create_user(self) -> list:
        print("Query from database...")
        query = QSqlQuery(self.db)
        query.prepare("SELECT * FROM users WHERE username = ? AND password = ?")
        query.addBindValue(f'{self.username_input.text()}')
        query.addBindValue(f'{self.password_input.text()}')
        users = []

        if query.exec():
            while query.next():
                print(query.value(1))
                name = query.value(1)
                auth = query.value(7)
                users.append((name, auth))
        else:
            print("Error fetching users:", query.lastError().text())
            
        if users == []:
            QMessageBox.warning(self, "Warning", "Non existing user or wrong password")
        else:
            print(users)
            return users
        
    def show_password(self, widget) -> None:
        if widget.echoMode() == QLineEdit.EchoMode.Normal:
            widget.setEchoMode(QLineEdit.EchoMode.Password)
            self.sender().setIcon(QIcon(self.show_icon))
        else:
            widget.setEchoMode(QLineEdit.EchoMode.Normal)
            self.sender().setIcon(QIcon(self.hide_icon))
            
    def show_register(self):
        print("Go to login - it will mean to close this dialog")


if __name__ == "__main__":
    app = QApplication([])
    dialog = RegistrationDialog()
    dialog.exec()
    app.exec()