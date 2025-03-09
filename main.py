"""
This is the main file of a library app.
It contains the main class and main functions.
"""
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,\
QLabel, QLineEdit, QComboBox, QTableWidget
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtCore import QSize
from sqlconnector import create_connection
import os, sys

class LibraryApp(QMainWindow):
    def __init__(self) -> None:
      super().__init__()
      
      self.script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
      
      self.initUi()
    
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
        self.login_action.triggered.connect(lambda: self.print_message('login'))
        
        self.logout_action = QAction('Logout', self)
        self.logout_action.triggered.connect(self.logout)
        
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
        
        # Main page search section
        self.filter_area = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to filter...")
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Filter by")
        # self.fill_filter_combo()
        
        self.order_by_combo = QComboBox()
        self.order_by_combo.addItem("Order by")
        # self.fill_order_by_combo()
        
        # Add elements to filter area
        self.filter_area.addWidget(self.search_input)
        self.filter_area.addWidget(self.filter_combo)
        self.filter_area.addWidget(self.order_by_combo)
        
        self.results_table = QTableWidget()
        
        self.main_page_layout.addLayout(self.filter_area)
        self.main_page_layout.addWidget(self.results_table)
        
        # Add elements to central widget
        self.central_widget.addWidget(self.welcome_page)
        self.central_widget.addWidget(self.main_page)

        self.setCentralWidget(self.central_widget)
        self.central_widget.setCurrentIndex(1)
        
    def print_message(self, message):
        # print('open')
        print(message)
        
    def fill_combo(self):
        raise NotImplementedError("Not implemented yet")
    
    def logout(self):
        self.central_widget.setCurrentIndex(0)
      
    
    
if __name__ == "__main__":
    app = QApplication([])

    if not create_connection('QSQLITE'):
        sys.exit(1)

    window = LibraryApp()
    window.show()

    app.exec()