from PyQt6.QtWidgets import QApplication, QDialog, QFormLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import os
import sys
import hashlib
from sqlconnector import create_connection
from clikc_label import ClickableLabel
from registration import RegistrationDialog

class LoginDialog(QDialog):
    accepted_signal = pyqtSignal(dict)
    
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

        self.mian_layout = QFormLayout(self)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.show_password_button = QPushButton(self)
        self.show_password_button.setIcon(QIcon(self.show_icon))
        self.show_password_button.setAutoDefault(False)
        self.show_password_button.clicked.connect(self.show_password)
        
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.show_password_button)

        login_button = QPushButton("Login", self)
        login_button.clicked.connect(self.login_user)
        
        label = QLabel("Don't have an account?")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        to_reg_form = ClickableLabel("Create account")
        to_reg_form.setAlignment(Qt.AlignmentFlag.AlignCenter)
        to_reg_form.clicked_signal.connect(self.show_register)

        self.mian_layout.addRow(self.username_input)
        self.mian_layout.addRow(self.password_input, self.show_password_button)
        self.mian_layout.addRow(login_button)
        self.mian_layout.addRow(label)
        self.mian_layout.addRow(to_reg_form)

    # Methods
    def login_user(self) -> list:
        if self.username_input.text() == "" or self.password_input.text() == "":
            QMessageBox.information(self, "Empty fields", "Username or password field is empty!")
            return []
        query = QSqlQuery(self.db)
        query.prepare("SELECT * FROM users WHERE username = ? AND password = ?")
        query.addBindValue(f'{self.username_input.text()}')
        query.addBindValue(f'{self.password_input.text()}')
        user = {"username": "", "authority": ""}

        if query.exec():
            while query.next():
                name = query.value(1)
                auth = query.value(7)
                user.update({"username": name})
                user.update({"authority": auth})
        else:
            print("Error fetching users:", query.lastError().text())

        if user["username"] == "":
            QMessageBox.warning(self, "Warning", "Non existing user or wrong password")
            self.username_input.setText("")
            self.password_input.setText("")
        else:
            self.accept()
        self.accepted_signal.emit(user)
        
    def show_password(self) -> None:
        if self.password_input.echoMode() == QLineEdit.EchoMode.Normal:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_password_button.setIcon(QIcon(self.show_icon))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_password_button.setIcon(QIcon(self.hide_icon))
            
    def show_register(self):
        print("Go to registration form")
        registration = RegistrationDialog()
        registration.exec()


if __name__ == "__main__":
    app = QApplication([])
    dialog = LoginDialog()
    dialog.exec()
    sys.exit(1)
    app.exec()