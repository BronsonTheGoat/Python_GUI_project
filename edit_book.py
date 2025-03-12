from PyQt6.QtWidgets import QApplication, QDialog, QTabWidget, QWidget, QVBoxLayout, QFormLayout, QLabel, QPushButton
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from sqlconnector import create_connection
import sys

class EditBookDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        # if create_connection("QSQLITE", "library"):
        #     print("Connected succesfully.")
        #     self.db = QSqlDatabase.database()
        #     if not self.db.isOpen():
        #         print("Database is not open!")
        # else:
        #     print("Connection failed")
                
        # tabwidget for the 3 different option
        # Edit Delete Add new
        
        # List all the attributes and add a button to do the corresponding action
        # The listing could be one method for all tabs as the button creation then
        # in an other method the action could be selected
        
        self.resize(400, 300)
        
        self.main_layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget(self)

        self.add_tab = QWidget()
        self.modify_tab = QWidget()
        self.delete_tab = QWidget()

        self.tabs.addTab(self.add_tab, "Add book")
        self.tabs.addTab(self.modify_tab, "Edit book")
        self.tabs.addTab(self.delete_tab, "Delete book")
        
        for i in range(self.tabs.count()):
            self.setup_tab(i)
        
        self.main_layout.addWidget(self.tabs)
        
    def setup_tab(self, i):
        tab = self.tabs.widget(i)
        btn_text = self.tabs.tabText(i).split(" ")[0]
        
        layout = QFormLayout()
        button = QPushButton(btn_text)
        button.clicked.connect(self.perform_action)

        layout.addRow(button)
        tab.setLayout(layout)
        
    def perform_action(self):
        print(self.sender().text())

if __name__ == "__main__":
    app = QApplication([])
    dialog = EditBookDialog()
    dialog.exec()
    sys.exit(1)
    app.exec()