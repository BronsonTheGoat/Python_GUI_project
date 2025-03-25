"""
This is the main file of a library app.
It contains the main class and main functions.
"""
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,\
QLabel, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QSpinBox, QFrame, QFileDialog
from PyQt6.QtGui import QAction, QIcon, QPixmap, QColor
from PyQt6.QtCore import QSize, Qt, QTimer, QDateTime
from db_handler import DatabaseHandler
from login import LoginDialog
from dashboard import DashboardDialog
from edit_book import EditBookDialog
import os
import sys
import csv

class LibraryApp(QMainWindow):
    def __init__(self, conn) -> None:
        super().__init__()
      
        self.script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.session = {"user": "",
                        "auth":"",
                        "started": False}
        
        self.selected_book:dict = {}
      
        self.db = conn
        if not self.db.get_db().isOpen():
            print("Database is not open!")
        
        self.initUi()
        QTimer.singleShot(200, self.login)
    
    # Methods
    def initUi(self) -> None:
        self.setWindowTitle("Library app")
        self.setFixedSize(QSize(1200, 600))
        self.setWindowIcon(QIcon(f"{self.script_directory}/assets/books.png"))
        
        # Menu
        self.menubar = self.menuBar()

        self.file_menu = self.menubar.addMenu("File")
        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Alt+F4")
        self.exit_action.setStatusTip("Exit application")
        self.exit_action.triggered.connect(self.close)

        self.login_action = QAction("Login", self)
        self.login_action.triggered.connect(self.login)
        
        self.logout_action = QAction("Logout", self)
        self.logout_action.triggered.connect(self.logout)
        self.logout_action.setVisible(False)
        
        self.dashboard_action = QAction("Dashboard", self)
        self.dashboard_action.triggered.connect(self.show_dashboard)
        self.dashboard_action.setVisible(False)
        
        self.save_menu = self.menubar.addMenu("Save")
        self.save_action = QAction("Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_file_dialog)
        self.save_action.setVisible(False)

        self.file_menu.addAction(self.login_action)
        self.file_menu.addAction(self.logout_action)
        self.file_menu.addAction(self.dashboard_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)
        
        self.save_menu.addAction(self.save_action)
    
        # Main layout
        self.central_widget = QStackedWidget()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(1000)  # milliseconds

        # Welcome page
        self.welcome_page = QWidget()
        self.welcome_page_layout = QVBoxLayout()
        self.welcome_page.setLayout(self.welcome_page_layout)
        
        self.welcome_image = "library.jpg"
        self.welcome_backround = QLabel()
        self.pixmap = QPixmap(f"{self.script_directory}/assets/{self.welcome_image}")
        self.pixmap = self.pixmap.scaled(int(self.width()), int(self.pixmap.height()*(self.width()/self.pixmap.width())))
        self.welcome_backround.setPixmap(self.pixmap)
        
        self.main_text = QLabel("Library app")
        self.main_text.setStyleSheet("font-family: 'Sans Serif'; font-size: 36px;")
        self.main_text.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.welcome_page_layout.addWidget(self.main_text)
        self.welcome_page_layout.addWidget(self.welcome_backround)

        # Main page
        self.main_page = QWidget()
        self.main_page_layout = QVBoxLayout()
        self.main_page.setLayout(self.main_page_layout)
        
        # main header area - header
        self.header = QHBoxLayout()
        
        self.welcome_text = QLabel(self)
        self.welcome_text.setStyleSheet("font-size: 24px;")
        self.welcome_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.clock = QLabel(self)
        self.clock.setText("current date - time")
        self.clock.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.header.addWidget(self.welcome_text)
        self.header.addWidget(self.clock)
        
        # Main page search section
        # TODO: add more option to filter the results
        self.filter_area = QHBoxLayout()
        
        self.filter_lines = QVBoxLayout()
        
        self.filter_line_fields = QHBoxLayout()
        self.filters = [self.filter_line_fields]
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to filter...")
        self.search_input.textChanged.connect(self.show_filtered_records)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Filter by --")
        self.filter_combo.currentTextChanged.connect(self.show_filtered_records)
        
        self.add_filter_button = QPushButton()
        self.add_filter_button.setText("Add filter")
        self.add_filter_button.clicked.connect(self.add_filter)
        
        self.order_by_combo = QComboBox()
        self.order_by_combo.addItem("Order by --")
        self.order_by_combo.currentTextChanged.connect(self.show_filtered_records)
        
        self.number_of_records = QSpinBox(self)
        self.number_of_records.setValue(13)
        self.number_of_records.setMinimum(1)   # default 0
        self.number_of_records.setMaximum(200)  # default 99
        self.number_of_records.valueChanged.connect(self.show_filtered_records)
        
        # Add elements to filter area
        self.filter_line_fields.addWidget(self.search_input)
        self.filter_line_fields.addWidget(self.filter_combo)
        self.filter_line_fields.addWidget(self.add_filter_button)
        self.filter_lines.addLayout(self.filter_line_fields)
        self.filter_area.addLayout(self.filter_lines)
        self.filter_area.addWidget(self.order_by_combo)
        self.filter_area.addWidget(QLabel("Shown results: "))
        self.filter_area.addWidget(self.number_of_records)
        
        # Edit area - shown only for admins and super admin
        self.edit_area = QFrame()
        self.edit_area_layout = QHBoxLayout()
        
        self.edit_book_button = QPushButton("Edit book", self)
        self.edit_book_button.clicked.connect(self.add_edit_book)
        
        self.add_book_button = QPushButton("Add new book", self)
        self.add_book_button.clicked.connect(self.add_edit_book)
        
        self.delete_book_button = QPushButton("Delete book", self)
        self.delete_book_button.clicked.connect(self.delete_book)
        
        self.edit_area_layout.addWidget(self.add_book_button)
        self.edit_area_layout.addWidget(self.edit_book_button)
        self.edit_area_layout.addWidget(self.delete_book_button)
        
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
        
    def update_label(self) -> None:
        """
        Updates the specified label with the current date and time
        """
        self.clock.setText(f'{QDateTime.currentDateTime().toString()}')
        
    def login(self) -> None:
        """
        Opens a dialog then starts a session if the login method returns successfully
        """
        login = LoginDialog(self.db)
        login.accepted_signal.connect(self.set_session)
        response = login.exec()
        
        if response:
            self.welcome_text.setText(f"Welcome {self.session["user"]}!")
            self.login_action.setVisible(False)
            self.logout_action.setVisible(True)
            self.save_action.setVisible(True)                
            self.show_hide_elements()
            self.fill_combo()
            self.fill_table()
            self.central_widget.setCurrentIndex(1)
            
        else:
            self.session["user"] = ""
            self.session["auth"] = ""
            self.session["started"] = False
            
    def show_dashboard(self) -> None:
        """
        Opens the dashboard dialog
        """
        dashboard = DashboardDialog(self.db, self.session)
        dashboard.exec()
        
    def save_file_dialog(self) -> None:
        """
        Opens a file dialog to prepare the saving of the results
        """
        file_dialog = QFileDialog(self)
        self.file_name, _ = file_dialog.getSaveFileName(caption="Save File", filter="*.csv")
        if self.file_name != "":
            extension = ".csv" if not ".csv" in self.file_name else ""
            self.save_result(self.file_name, extension)
            
    def save_result(self, file_name: str, extension: str) -> None:
        """
        Performs the saving of the search results.

        Args:
            file_name (str): The name of the outpu file
            extension (str): The extension of the output file. It is alway .csv
        """
        print("Saving search result...")
        list, headers = self.current_list()
        with open(f"{file_name}{extension}", "w", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(list)
            
    def current_list(self) -> list[list[dict[str:str]], list[str]]:
        """
        Creates a list of dictionaries based on the shown search results.
        And a list of the column headers.

        Returns:
            list: Contains dictionaries where the column headers are the keys, the values are the corresponding book data. 
        """
        field_names: list[str] =  [self.filter_combo.itemText(i) for i in range(1,self.filter_combo.count())]
        search_result: list[dict[str:str]] = []
        for i in range(self.results_table.rowCount()):
            row = {field_names[column]:self.results_table.item(i, column).text() for column in range(1,self.results_table.columnCount())}
            search_result.append(row)
            row = {}
        return search_result, field_names
            
    def set_session(self, user: dict[str, str]) -> None:
        """
        Creates a dictionary called session with the actually logged in user's data.
        
        Args:
            user (dict[str, str]): A dictionary contais the necessary data t create a session dict: username and authority
        """
        self.session["user"] = user["username"]
        self.session["auth"] = user["authority"]
        self.session["started"] = True
        
    def show_hide_elements(self) -> None:
        """
        Show or hide the elements which are only can seen by the authenticated user.
        """
        enabled: dict[str,list[str]] = {"user": [False, False],
                                        "admin": [True, False],
                                        "superadmin": [True, True]}
        self.edit_area.setVisible(enabled.get(self.session["auth"])[0])        
        self.dashboard_action.setVisible(enabled.get(self.session["auth"])[1])
        
        
    def fill_combo(self) -> None:
        """
        Gets the column names from the database then sets them as filter and oredring options.
        """
        query_txt = "PRAGMA table_info (books)"
        self.headers = self.db.fetch(query_txt)
        for row in self.headers:
            self.filter_combo.addItem(row[1])
            self.order_by_combo.addItem(row[1])
            
    def get_data_from_db(self, sql_query, params = None) -> list[str|int|bool]:
        """
        Fetch data from dtabase

        Args:
            sql_query (str): An SQL query string (SQLite)
            params (list|tuple, optional): Values for the SQL query. Defaults to None.

        Returns:
            list[str|int|bool]: The fetched records in a list.
        """
        # filter_field = self.filter_combo.currentText()
        # filter_text = self.search_input.text()
        # filter = f"%{filter_text}%" if filter_text != "" and "--" not in filter_field else None
        if params:
            filter = [f"%{filter_text}%" for filter_text in params]
        else:
            filter = params
        records = self.db.fetch(sql_query, filter)
        if filter:
            self.number_of_records.setValue(len(records))
        else:
            self.number_of_records.setValue(13)
        return records
            
    def fill_table(self, query="SELECT * FROM books", params = None) -> None:
        """
        Fills the central table with the records fethced from the database.
        """        
        self.results_table.setRowCount(self.number_of_records.value())
        self.results_table.setColumnCount(self.filter_combo.count()-1)
        
        headers = [self.filter_combo.itemText(i) for i in range(1,self.filter_combo.count())]
        self.results_table.setHorizontalHeaderLabels(headers)
        
        self.data = self.get_data_from_db(query, params)
        
        for row, column in enumerate(self.data):
            for col in range(self.results_table.columnCount()):
                self.results_table.setItem(row, col, QTableWidgetItem(str(column[col])))
                
        self.results_table.cellClicked.connect(self.cell_clicked)
        self.originalBg = self.results_table.horizontalHeaderItem(0).background()
        
    def cell_clicked(self, row: int) -> None:
        """
        Highlights the row of thr clicked cell or removes the highlight.

        Args:
            row (int): The number of the clicked cell's row.
        """
        if row in self.selected_book.keys():
            self.set_color_to_row(row, self.originalBg)
            self.selected_book = {}
        elif len(self.selected_book) > 0:
            self.set_color_to_row(list(self.selected_book.keys())[0], self.originalBg)
            self.selected_book = {}
            self.selected_book = {row:[self.results_table.item(row, column).text() for column in range(self.results_table.columnCount())]}
            self.set_color_to_row(row, QColor("green"))
        else:
            self.selected_book = {row:[self.results_table.item(row, column).text() for column in range(self.results_table.columnCount())]}
            self.set_color_to_row(row, QColor("green"))           
            
    def set_color_to_row(self, rowIndex: int, color: QColor) -> None:
        """
        Sets the given color to all the cells in the correponding row.

        Args:
            rowIndex (int): The number of the row which background-color should be changed.
            color (QColor): The color which will be setted as background-color.
        """
        for j in range(self.results_table.columnCount()):
            self.results_table.item(rowIndex, j).setBackground(color)
    
    def show_filtered_records(self) -> None:
        """
        Based on the setted filtes collects the data from the databse and shows it in the central table.
        """
        order_by = "id" if "--" in self.order_by_combo.currentText() else self.order_by_combo.currentText()
        query = "SELECT * FROM books"
        layout: list = self.filter_lines.children()
        filters = {}
        for item in layout:
            combo = item.itemAt(1).widget()
            filter_text = item.itemAt(0).widget().text()
            filter_field_name = combo.currentText()
            if not "--" in filter_field_name and filter_text != "":
                filters[filter_field_name] = filter_text
                
            # Set selected items inactive in the other comboboxes
            # if combo != self.sender() and not "--" in self.sender().currentText():
            #     combo.setItemData(self.sender().currentIndex(), Qt.ItemFlag.ItemIsEnabled, Qt.ItemDataRole.UserRole - 1)
            # else:
            #     combo.setItemData(self.sender().currentIndex(), 0, Qt.ItemDataRole.UserRole - 1)
                
        if  filters:
            query += f" WHERE {' AND '.join([field_name + ' LIKE ? ' for field_name in filters.keys()])} ORDER BY {order_by}"
            print(query)
        else:
            query += f" ORDER BY {order_by}"
        
        self.results_table.clear()
        self.fill_table(query, filters.values() if filters != {} else None)
        
    def logout(self) -> None:
        """
        Logging out ht eactual user and sets the UI to default state.
        """
        self.central_widget.setCurrentIndex(0)
        self.login_action.setVisible(True)
        self.logout_action.setVisible(False)
        self.save_action.setVisible(False)
        
    def add_edit_book(self) -> None:
        """
        Opens the edit/add dialog.
        """
        headers = [self.results_table.horizontalHeaderItem(c).text() for c in range(self.results_table.columnCount())]
        page = self.sender().text().split(" ")[0]
        data = list(self.selected_book.values())[0] if self.selected_book else []
        edit_books = EditBookDialog(self.db, fields=headers, tab_name=page, data=data)
        edit_books.exec()
        
    def delete_book(self) -> None:
        """
        Deletes the selcted book from the database and refresh the data in the table.
        """
        if len(self.selected_book) > 0:
            buttons = QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Yes
            user_choice = QMessageBox.critical(self, "Warning!",
                                """You are trying to delete a book from the database!\n
                                    There's no possibility to undo this move!\n
                                    Are you sure about this?""", buttons)
            if user_choice == QMessageBox.StandardButton.Yes:
                print(f"Book deleted successfully from database... {list(self.selected_book.values())[0][0]}")
                query_text: str = "DELETE FROM books WHERE id = ?"
                self.db.execute_non_query(query_text, list(self.selected_book.values())[0][0])
                self.selected_book = {}
                self.show_filtered_records()
            else:
                print("User dcided to keep the book.")
        else:
            QMessageBox.information(self, "No book selected", "Please select a book to perform this action!")
    
    def add_filter(self) -> None:
        """
        Creates a new row with an input field, a dropdown with the colum names (book properties) and a remove button.
        """
        if len(self.filters) < 4:
            filter_line_fields = QHBoxLayout()
                    
            search_input = QLineEdit()
            search_input.setPlaceholderText("Type to filter...")
            search_input.textChanged.connect(self.show_filtered_records)
            
            filter_combo = QComboBox()
            filter_combo.addItem("Filter by --")
            # TODO: need to inactivate all the items which are already in use and need to mxaimize No of filters
            for row in self.headers:
                filter_combo.addItem(row[1])
            filter_combo.currentTextChanged.connect(self.show_filtered_records)
            
            add_filter_button = QPushButton()
            add_filter_button.setText("Remove filter")
            add_filter_button.clicked.connect(self.remove_filter)
            
            filter_line_fields.addWidget(search_input)
            filter_line_fields.addWidget(filter_combo)
            filter_line_fields.addWidget(add_filter_button)
            self.filter_lines.addLayout(filter_line_fields)
            self.filters.append(filter_line_fields)
        else:
            QMessageBox.information(self, "Filters limited", "You can not add more filters")
    
    def remove_filter(self) -> None:
        """
        Removes the correponding line of filter input.
        """
        print(self.sender())
        layout: list = self.filter_lines.children() #self.sender().parent().layout().children()[1].layout().children()[0].layout().children()
        for item in layout:
            if item.itemAt(2).widget() == self.sender():
                for i in reversed(range(item.count())): 
                    item.itemAt(i).widget().setParent(None)
                self.filter_lines.removeItem(item)
                self.filters.remove(item)
    
if __name__ == "__main__":
    app = QApplication([])

    if not DatabaseHandler():
        QMessageBox.critical("Error", "Databasse is not available!")
        sys.exit(1)
    else:
        conn = DatabaseHandler()
        
    window = LibraryApp(conn)
    app.exec()