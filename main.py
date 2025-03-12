"""
This is the main file of a library app.
It contains the main class and main functions.
"""
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,\
QLabel, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QSpinBox, QFrame
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from sqlconnector import create_connection
from login import LoginDialog
import os
import sys

class LibraryApp(QMainWindow):
    def __init__(self) -> None:
      super().__init__()
      
      self.script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
      self.session = {"user": "",
                      "auth":"",
                      "started": False}
      
      self.db = QSqlDatabase.database()
      if not self.db.isOpen():
        print("Database is not open!")
      
      self.initUi()
    #   self.fill_combo()
    #   self.fill_table()
    
    # Methods
    def initUi(self) -> None:
        self.setWindowTitle("Library app")
        self.setFixedSize(QSize(800, 600))
        self.setWindowIcon(QIcon(f"{self.script_directory}/assets/books.png"))
        
        # Menu
        self.menubar = self.menuBar()

        self.file_menu = self.menubar.addMenu('File')
        self.exit_action = QAction('Exit', self)
        self.exit_action.setShortcut('Alt+F4')
        self.exit_action.setStatusTip('Exit application')
        self.exit_action.triggered.connect(self.close)

        self.login_action = QAction('Login', self)
        self.login_action.triggered.connect(self.login)
        
        self.logout_action = QAction('Logout', self)
        self.logout_action.triggered.connect(self.logout)
        self.logout_action.setVisible(False)
        
        self.dashboard_action = QAction('Dashboard', self)
        self.dashboard_action.triggered.connect(lambda: self.print_message('dashboard'))

        self.file_menu.addAction(self.login_action)
        self.file_menu.addAction(self.logout_action)
        self.file_menu.addAction(self.dashboard_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)
    
        # Main layout
        self.central_widget = QStackedWidget()

        # Welcome page
        self.welcome_page = QWidget()
        self.welcome_page_layout = QVBoxLayout()
        self.welcome_page.setLayout(self.welcome_page_layout)
        
        self.welcome_image = "library_small.jpg"
        self.welcome_backround = QLabel()
        self.pixmap = QPixmap(f"{self.script_directory}/assets/{self.welcome_image}")
        # Set pixmap width and height maximum 800 x 600 px
        # self.pixmap_width = self.set_pixmap_width()
        # self.pixmap_heoght = self.set_pixmap_height()
        # self.pixmap = pixmap.scaled(int(pixmap.width()/2), int(pixmap.height()/2))
        self.welcome_backround.setPixmap(self.pixmap)
        
        self.welcome_page_layout.addWidget(self.welcome_backround)

        # Main page
        self.main_page = QWidget()
        self.main_page_layout = QVBoxLayout()
        self.main_page.setLayout(self.main_page_layout)
        
        # main header area - header
        self.header = QHBoxLayout()
        
        self.welcome_text = QLabel(self)
        
        self.clock = QLabel(self)
        self.clock.setText("current date - time")
        self.clock.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.header.addWidget(self.welcome_text)
        self.header.addWidget(self.clock)
        
        # Main page search section
        # TODO: add more option to filter the results
        self.filter_area = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to filter...")
        self.search_input.textChanged.connect(self.create_filter_query)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Filter by --")
        self.filter_combo.currentTextChanged.connect(self.create_filter_query)
        
        self.order_by_combo = QComboBox()
        self.order_by_combo.addItem("Order by --")
        self.order_by_combo.currentTextChanged.connect(self.create_filter_query)
        
        self.number_of_records = QSpinBox(self)
        self.number_of_records.setValue(14)
        self.number_of_records.setMinimum(1)   # default 0
        self.number_of_records.setMaximum(100)  # default 99
        self.number_of_records.valueChanged.connect(self.create_filter_query)
        
        # Add elements to filter area
        self.filter_area.addWidget(self.search_input)
        self.filter_area.addWidget(self.filter_combo)
        self.filter_area.addWidget(self.order_by_combo)
        self.filter_area.addWidget(QLabel("Shown results: "))
        self.filter_area.addWidget(self.number_of_records)
        
        # Edit area - shown only for admins and super admin
        self.edit_area = QFrame()
        self.edit_area_layout = QHBoxLayout()
        
        self.edit_book_button = QPushButton("Edit book", self)
        self.edit_book_button.clicked.connect(self.edit_book)
        
        self.add_book_button = QPushButton("Add new book", self)
        self.add_book_button.clicked.connect(self.add_book)
        
        self.edit_area_layout.addWidget(self.add_book_button)
        self.edit_area_layout.addWidget(self.edit_book_button)
        
        self.edit_area.setLayout(self.edit_area_layout)
        
        # Results shown in table or as widgets with thumbnail
        self.results_table = QTableWidget()
        
        # Set main layout
        self.main_page_layout.addLayout(self.header)
        self.main_page_layout.addLayout(self.filter_area)
        self.main_page_layout.addWidget(self.edit_area)
        self.main_page_layout.addWidget(self.results_table)
        
        # Add elements to central widget
        self.central_widget.addWidget(self.welcome_page)
        self.central_widget.addWidget(self.main_page)

        self.setCentralWidget(self.central_widget)
        self.central_widget.setCurrentIndex(0)
        
        self.show()
        
    def print_message(self, message):
        # print('open')
        print(message)
        
    def login(self):
        login = LoginDialog(self)
        login.accepted_signal.connect(self.set_session)
        response = login.exec()
        # print(self.session)
        
        if response:
            self.welcome_text.setText(f"Welcome {self.session["user"]}!")
            self.login_action.setVisible(False)
            self.logout_action.setVisible(True)
            if self.session["auth"] not in ("admin", "superadmin"):
                enabled: bool = False
            self.show_hide_elements(enabled)
            self.fill_combo()
            self.fill_table()
            self.central_widget.setCurrentIndex(1)
            
        else:
            self.session["user"] = ""
            self.session["auth"] = ""
            self.session["started"] = False
            
    def set_session(self, user):
        self.session["user"] = user["username"]
        self.session["auth"] = user["authority"]
        self.session["started"] = True
        
    def show_hide_elements(self, enabled: bool = True):
        self.dashboard_action.setVisible(enabled)
        self.edit_area.setVisible(enabled)
        
        
    def fill_combo(self):
        query = QSqlQuery(self.db)
        query.prepare("PRAGMA table_info (books)")

        if query.exec():
            while query.next():
                self.filter_combo.addItem(query.value(1))
                self.order_by_combo.addItem(query.value(1))
        else:
            print("Error fetching books:", query.lastError().text())
            
    def get_data_from_db(self, sql_query, columns):
        query = QSqlQuery(self.db)
        query.prepare(sql_query)
        filter_field = self.filter_combo.currentText()
        filter_text = self.search_input.text()
        if filter_text != "" and "--" not in filter_field:
            query.addBindValue(f'%{filter_text}%')
        records = []
        
        if query.exec():
            while query.next():
                line = []
                for i in range(columns):
                    line.append(query.value(i))
                records.append(line)                
        else:
            print("Error fetching books:", query.lastError().text())
            
        return records
            
    def fill_table(self, query="SELECT * FROM books"):        
        self.results_table.setRowCount(self.number_of_records.value())
        self.results_table.setColumnCount(self.filter_combo.count()-1)
        
        headers = [self.filter_combo.itemText(i) for i in range(1,self.filter_combo.count())]
        self.results_table.setHorizontalHeaderLabels(headers)
        
        data = self.get_data_from_db(query, len(headers))
        
        for row, column in enumerate(data):
            for col in range(self.results_table.columnCount()):
                self.results_table.setItem(row, col, QTableWidgetItem(str(column[col])))
                
    #     self.results_table.cellClicked.connect(self.cell_clicked)
        
    # def cell_clicked(self):
    #     raise NotImplementedError("Method not implemented")
    
    def create_filter_query(self):        
        order_by = "id" if "--" in self.order_by_combo.currentText() else self.order_by_combo.currentText()
        query = "SELECT * FROM books"
        if not "--" in self.filter_combo.currentText() and self.search_input.text() != "":
            query += f" WHERE {self.filter_combo.currentText()} LIKE ? ORDER BY {order_by}"
        else:
            query += f" ORDER BY {order_by}"
        
        self.results_table.clear()
        self.fill_table(query)
        
    def logout(self):
        self.central_widget.setCurrentIndex(0)
        self.login_action.setVisible(True)
        self.logout_action.setVisible(False)
        
    def edit_book(self):
        raise NotImplementedError("Not implemented yet")
    
    def add_book(self):
        raise NotImplementedError("Not implemented yet")
      
    
    
if __name__ == "__main__":
    app = QApplication([])

    if not create_connection('QSQLITE', "library"):
        QMessageBox.critical("Error", "Databasse is not available!")
        sys.exit(1)

    window = LibraryApp()
    app.exec()