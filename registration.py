from PyQt6.QtWidgets import QApplication, QDialog, QFormLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox, QDateEdit
from PyQt6.QtGui import QPixmap, QIcon, QRegularExpressionValidator, QPalette, QColor
from PyQt6.QtCore import pyqtSignal, Qt, QRegularExpression, QDate
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

        self.main_layout = QFormLayout(self)
        
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Name")
        self.name_input.textChanged.connect(self.check_all_fields_filled)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.textChanged.connect(self.check_all_fields_filled)
        
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setToolTip("Password should have at least 8 character\nand one capital letter and one number.")
        
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

        password_regex = QRegularExpression(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$')
        pw_validator = QRegularExpressionValidator(password_regex, self.password_input)
        self.password_input.setValidator(pw_validator)
        self.password_input.textChanged.connect(lambda: self.validate_input(self.password_input))
        pw_2_validator = QRegularExpressionValidator(password_regex, self.password_input)
        self.password_2_input.setValidator(pw_2_validator)
        self.password_2_input.textChanged.connect(lambda: self.validate_input(self.password_2_input))
        
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_2_input)
        password_layout.addWidget(self.show_password_2_button)
        
        # TODO: brth date as date edit
        
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        
        email_regex = QRegularExpression(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        email_validator = QRegularExpressionValidator(email_regex, self.email_input)
        self.email_input.setValidator(email_validator)
        self.email_input.textChanged.connect(lambda: self.validate_input(self.email_input))
        
        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Phone")
        
        phone_regex = QRegularExpression(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$')
        phone_validator = QRegularExpressionValidator(phone_regex, self.phone_input)
        self.phone_input.setValidator(phone_validator)
        self.phone_input.textChanged.connect(lambda: self.validate_input(self.phone_input))
        
        self.birth_input = QDateEdit()
        self.birth_input.setDate(QDate(2024, 8, 3))
        self.birth_input.setDisplayFormat('yyyy-MM-dd')
        self.birth_input.setCalendarPopup(True)
        self.birth_input.setMaximumDate(QDate.currentDate().addYears(-6))
        self.birth_input.setToolTip("You must be a tleast 6 years old to register.")

        self.login_button = QPushButton("Create account", self)
        self.login_button.clicked.connect(self.create_user)
        self.login_button.setEnabled(False)
        
        self.label = QLabel("Already have an account??")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        to_reg_form = ClickableLabel("Login")
        to_reg_form.setAlignment(Qt.AlignmentFlag.AlignCenter)
        to_reg_form.clicked_signal.connect(self.show_register)

        self.main_layout.addRow(self.name_input)
        self.main_layout.addRow(self.username_input)
        self.main_layout.addRow(self.password_input, self.show_password_button)
        self.main_layout.addRow(self.password_2_input, self.show_password_2_button)
        self.main_layout.addRow(self.email_input)
        self.main_layout.addRow(self.phone_input)
        self.main_layout.addRow(self.birth_input)
        self.main_layout.addRow(self.login_button)
        self.main_layout.addRow(self.label)
        self.main_layout.addRow(to_reg_form)

    # Methods
    def create_user(self) -> list:
        print("Query from database...")
        query = QSqlQuery(self.db)
        query.prepare("SELECT * FROM users WHERE username = ? AND password = ?")
        query.addBindValue(f'{self.username_input.text()}')
        query.addBindValue(f'{self.password_input.text()}')
        users: list = []

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
        self.close()
        
    def check_all_fields_filled(self):
        widgets = (self.main_layout.itemAt(i).widget() for i in range(self.main_layout.count())) 
        for widget in widgets:
            if isinstance(widget, QLineEdit):
                print(f"linedit: {widget.objectName()} - {widget.text()}")
        
    def validate_input(self, widget) -> None:
        self.set_input_valid(widget.hasAcceptableInput(), widget)
        self.check_all_fields_filled()
        
    def set_input_valid(self, is_valid: bool, widget) -> None:
        palette = widget.palette()
        if is_valid:
            palette.setColor(QPalette.ColorRole.Base, QColor(220, 255, 220))
            widget.setStyleSheet("color: black;")
        else:
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 220, 220))
            widget.setStyleSheet("color: black;")

        widget.setPalette(palette)

if __name__ == "__main__":
    app = QApplication([])
    dialog = RegistrationDialog()
    dialog.exec()
    app.exec()