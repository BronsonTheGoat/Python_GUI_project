from PyQt6.QtWidgets import QApplication, QDialog, QTabWidget, QWidget, QVBoxLayout, QFormLayout, QLabel, QPushButton, QLineEdit
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from sqlconnector import create_connection
import sys

class EditBookDialog(QDialog):
    def __init__(self, fields: list, tab_name, data: list = [], parent=None) -> None:
        super().__init__(parent)
        
        # if create_connection("QSQLITE", "library"):
        #     print("Connected succesfully.")
        #     self.db = QSqlDatabase.database()
        #     if not self.db.isOpen():
        #         print("Database is not open!")
        # else:
        #     print("Connection failed")
        
        self.resize(400, 300)
        self.setWindowTitle("Add / modify book")
        
        self.fields: list[str] = fields
        self.data: list[str] = data if len(data) > 0 else ["" for _ in range(len(fields))]
        self.active_tab = self.set_default_tab(tab_name)
        
        self.main_layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget(self)

        self.add_tab = QWidget()
        self.modify_tab = QWidget()
        self.delete_tab = QWidget()

        self.tabs.addTab(self.add_tab, "Add book")
        self.tabs.addTab(self.modify_tab, "Edit book")
        
        for i in range(self.tabs.count()):
            self.setup_tab(i)
        
        self.tabs.setCurrentIndex(self.active_tab)
        
        self.main_layout.addWidget(self.tabs)
        
        self.set_default_tab(tab_name)
        
    def set_default_tab(self, tab_name: str) -> int:
        tab_functions: dict[str, int] = {"Add": 0,
                                "Edit": 1}
        return tab_functions.get(tab_name)
        
    def setup_tab(self, i: int) -> None:
        tab = self.tabs.widget(i)
        
        btn_text = self.tabs.tabText(i).split(" ")[0]
        
        layout = QFormLayout()
        
        for title, item in zip(self.fields, self.data):
            if self.fields.index(title) > 0:
                label = QLabel(title)
                input_book = QLineEdit()
                if self.active_tab == 1 and i == 1:
                    input_book.setText(item)
            
                layout.addRow(label, input_book)
        
        button = QPushButton(btn_text)
        button.clicked.connect(self.perform_action)

        layout.addRow(button)
        tab.setLayout(layout)
        
    def perform_action(self):
        print(self.sender().text())

if __name__ == "__main__":
    app = QApplication([])
    headers: list = ['id', 'isbn13', 'isbn10', 'title', 'subtitle', 'authors', 'categories', 'thumbnail', 'description', 'published_year', 'average_rating', 'num_pages', 'ratings_count']
    data: list = ['1', '9780002005883', '2005883', 'Gilead', '', 'Marilynne Robinson', 'Fiction', 'http://books.google.com/books/content?id=KQZCPgAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api', 'A NOVEL THAT READERS and critics have been eagerly anticipating for over a decade, Gilead is an astonishingly imagined story of remarkable lives. John Ames is a preacher, the son of a preacher and the grandson (both maternal and paternal) of preachers. It’s 1956 in Gilead, Iowa, towards the end of the Reverend Ames’s life, and he is absorbed in recording his family’s story, a legacy for the young son he will never see grow up. Haunted by his grandfather’s presence, John tells of the rift between his grandfather and his father: the elder, an angry visionary who fought for the abolitionist cause, and his son, an ardent pacifist. He is troubled, too, by his prodigal namesake, Jack (John Ames) Boughton, his best friend’s lost son who returns to Gilead searching for forgiveness and redemption. Told in John Ames’s joyous, rambling voice that finds beauty, humour and truth in the smallest of life’s details, Gilead is a song of celebration and acceptance of the best and the worst the world has to offer. At its heart is a tale of the sacred bonds between fathers and sons, pitch-perfect in style and story, set to dazzle critics and readers alike.', '2004', '3.85', '247', '361']
    dialog = EditBookDialog(headers, "Edit", data)
    dialog.exec()
    sys.exit(1)
    app.exec()