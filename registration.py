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
    
    input_widgets: dict = {}

    def __init__(self, conn, parent=None) -> None:
        super().__init__(parent)
        
        self.db = conn
        
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
        self.password_2_input.setToolTip("Be careful: Passwords must match!")
        
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
        self.password_2_input.textChanged.connect(lambda: self.validate_input(self.password_2_input, True))
        
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_2_input)
        password_layout.addWidget(self.show_password_2_button)
        
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

        self.registration_button = QPushButton("Create account", self)
        self.registration_button.clicked.connect(self.create_user)
        self.registration_button.setEnabled(False)
        
        self.label = QLabel("Already have an account??")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        to_reg_form = ClickableLabel("Login")
        to_reg_form.setAlignment(Qt.AlignmentFlag.AlignCenter)
        to_reg_form.clicked_signal.connect(self.self.close())

        self.main_layout.addRow(self.name_input)
        self.main_layout.addRow(self.username_input)
        self.main_layout.addRow(self.password_input, self.show_password_button)
        self.main_layout.addRow(self.password_2_input, self.show_password_2_button)
        self.main_layout.addRow(self.email_input)
        self.main_layout.addRow(self.phone_input)
        self.main_layout.addRow(QLabel("Birth date:"))
        self.main_layout.addRow(self.birth_input)
        self.main_layout.addRow(self.registration_button)
        self.main_layout.addRow(self.label)
        self.main_layout.addRow(to_reg_form)

    # Methods
    def create_user(self) -> None:
        user: dict = {"name": self.name_input.text(),
                "username": self.username_input.text(),
                "password": self.password_input.text(),
                "email": self.email_input.text(),
                "phone": self.phone_input.text(),
                "birth_date": self.birth_input.date().toString('yyyy-MM-dd'),
                "authorization": "user"
                }
        
        query_str: str = f"INSERT INTO users ({", ".join(user.keys())}) Values ({", ".join(["?" for _ in range(len(user))])})"
            
        registration = self.db.execute_non_query(query_str, user.values())
        
        if registration:
                print("User succesfully created")
                QMessageBox.information(self, "User created", "Your registration was succesful.\nYou can login now.")
        else:
            QMessageBox.warning(self, "Error", "For some reason the registration was incomplete.")
        
    def show_password(self, widget) -> None:
        if widget.echoMode() == QLineEdit.EchoMode.Normal:
            widget.setEchoMode(QLineEdit.EchoMode.Password)
            self.sender().setIcon(QIcon(self.show_icon))
        else:
            widget.setEchoMode(QLineEdit.EchoMode.Normal)
            self.sender().setIcon(QIcon(self.hide_icon))
        
    def check_all_fields_filled(self, valid) -> None:
        widgets_filled: list = all(widget.text().strip() != "" and valid for i in range(self.main_layout.count()) if isinstance(widget := self.main_layout.itemAt(i).widget(), QLineEdit))
        self.registration_button.setEnabled(widgets_filled)
        
    def password_match(self) -> bool:
        return self.password_input.text() == self.password_2_input.text()
        
    def validate_input(self, widget, is_password=False) -> None:
        if is_password:
            valid: bool = self.password_match() and widget.hasAcceptableInput()
        else:
            valid = widget.hasAcceptableInput()
        self.set_input_valid(valid, widget)
        self.check_all_fields_filled(valid)            
        
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
    sys.exit(1)
    app.exec()