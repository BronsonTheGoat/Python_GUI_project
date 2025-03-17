from PyQt6.QtWidgets import QApplication, QDialog, QTabWidget, QWidget, QVBoxLayout, QFormLayout, QLabel, QPushButton,\
    QLineEdit, QMessageBox
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from db_handler import DatabaseHandler
import sys

class EditBookDialog(QDialog):
    def __init__(self, conn, fields: list, tab_name, data: list = [], parent=None) -> None:
        super().__init__(parent)
        
        self.db = conn
        self.widgets_text: list = []
        
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
                    
                input_book.textChanged.connect(self.property_modified)
            
                layout.addRow(label, input_book)
        
        button = QPushButton(btn_text)
        button.clicked.connect(self.perform_action)

        layout.addRow(button)
        tab.setLayout(layout)
        
    def property_modified(self):
        # print(self.sender().parent().layout().count())
        parent_widget: int = self.sender().parent().layout()
        self.widgets_text = [widget.text() for i in range(parent_widget.count()) if isinstance(widget := parent_widget.itemAt(i).widget(), QLineEdit)]
        self.lables_text = [widget.text() for i in range(parent_widget.count()) if isinstance(widget := parent_widget.itemAt(i).widget(), QLabel)]
        index = self.widgets_text.index(self.sender().text())
        self.validate_field(self.sender(), index)
    
    def validate_field(self, widget, i):
        isbn_13_regex = QRegularExpression(r"[0-9]{13}")
        isbn_10_regex = QRegularExpression(r"([0-9]){9,10}(?:[A-Z]?$)")
        thumbnail_regex = QRegularExpression(r"/^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$/")
        published_year_regex = QRegularExpression(r"[0-9]{1,4}")
        average_rating_regex = QRegularExpression(r"[0-9]+\.[0-9]+")
        num_pages_regex = QRegularExpression(r"[0-9]+")
        ratings_count_regex = QRegularExpression(r"[0-9]+")
        validators: dict = {"isbn13": isbn_13_regex,
                            "isbn10": isbn_10_regex,
                            "thumbnail": thumbnail_regex,
                            "published_year": published_year_regex,
                            "average_rating": average_rating_regex,
                            "num_pages": num_pages_regex,
                            "ratings_count": ratings_count_regex
                            }
        if self.lables_text[i] in validators.keys():
            validator = QRegularExpressionValidator(validators.get(self.lables_text[i]), widget)
            widget.setValidator(validator)
            self.validate_input(widget)
        else:
            return
        
    def validate_input(self, widget) -> None:
        valid = widget.hasAcceptableInput()
        self.set_input_valid(valid, widget)
        
    def set_input_valid(self, is_valid: bool, widget) -> None:
        if is_valid:
            widget.setStyleSheet("background-color: green;")
        else:
            widget.setStyleSheet("background-color: red;")
    
    def check_empty_fields(self,sender):
        parent_widget_count: int = sender.parent().layout().count()
        all_filled: bool = all(widget.text().strip() for i in range(parent_widget_count) if isinstance(widget := self.sender().parent().layout().itemAt(i).widget(), QLineEdit))
        return all_filled

    def check_book_modified(self):
        if self.widgets_text != []:
            for original, modified in zip(self.data, self.widgets_text):
                if original != modified:
                    return True
                return False
        else:
            return False
        
    def perform_action(self):
        action: str = self.sender().text()
        match action:
            case "Add":
                if not self.check_empty_fields(self.sender()):
                    buttons = QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Apply
                    answer = QMessageBox.information(self, "Emptyfields", "There are empty fields.\nAre you sure about to continue?", buttons)
                    if answer == QMessageBox.StandardButton.Apply:
                        response = QMessageBox.question(self, "Add new book", "Are you sure about to add a new book to library?")
                        if response == QMessageBox.StandardButton.Yes:
                            print("User clicked Yes")
                            self.add_book()
                    else:
                        print("User clicked No")
                        # Just do  nothing        
            case "Edit":
                if self.check_book_modified():                
                    response = QMessageBox.question(self, "Modified data", "You modified the data of this book.\nAre you sur eto save the changes?")
                    if response == QMessageBox.StandardButton.Yes:
                        print("User clicked yes")
                        self.edit_book()
                else:
                    QMessageBox.information(self, "No modification", "You did'nt make any modification is the book data.\nThe previously stored vales will remain.")
        
    def add_book(self):
        query_text: str = f"INSERT INTO book ({" ,".join([i for i in self.fields if i != "id"])}) VALUES ({", ".join(["?" for _ in range(len(self.widgets_text))])})"
        print(query_text)
        self.db.execute_non_query(query_text, self.widgets_text)
        
    def edit_book(self):
        query_text: str = f"UPDATE book SET {",".join([field + ' = ?' for field in self.fields])} WHERE id = {data[0]}"
        edited = self.db.execute_non_query(query_text, self.widgets_text)
        if edited:
            QMessageBox.information(self, "Success", "Book updated successfully!")
        else:
            QMessageBox.warning(self, "Error", "Something went wrong.")
        
        # get field names and field values
        # TODO: INSERT adn UPDATE need to be implemented

if __name__ == "__main__":
    app = QApplication([])
    headers: list = ['id', 'isbn13', 'isbn10', 'title', 'subtitle', 'authors', 'categories', 'thumbnail', 'description', 'published_year', 'average_rating', 'num_pages', 'ratings_count']
    data: list = ['1', '9780002005883', '2005883', 'Gilead', '', 'Marilynne Robinson', 'Fiction', 'http://books.google.com/books/content?id=KQZCPgAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api', 'A NOVEL THAT READERS and critics have been eagerly anticipating for over a decade, Gilead is an astonishingly imagined story of remarkable lives. John Ames is a preacher, the son of a preacher and the grandson (both maternal and paternal) of preachers. It’s 1956 in Gilead, Iowa, towards the end of the Reverend Ames’s life, and he is absorbed in recording his family’s story, a legacy for the young son he will never see grow up. Haunted by his grandfather’s presence, John tells of the rift between his grandfather and his father: the elder, an angry visionary who fought for the abolitionist cause, and his son, an ardent pacifist. He is troubled, too, by his prodigal namesake, Jack (John Ames) Boughton, his best friend’s lost son who returns to Gilead searching for forgiveness and redemption. Told in John Ames’s joyous, rambling voice that finds beauty, humour and truth in the smallest of life’s details, Gilead is a song of celebration and acceptance of the best and the worst the world has to offer. At its heart is a tale of the sacred bonds between fathers and sons, pitch-perfect in style and story, set to dazzle critics and readers alike.', '2004', '3.85', '247', '361']
    if not DatabaseHandler():
        QMessageBox.critical("Error", "Databasse is not available!")
        sys.exit(1)
    else:
        conn = DatabaseHandler()
    dialog = EditBookDialog(conn,headers, "Edit", data)
    dialog.exec()
    sys.exit(1)
    app.exec()