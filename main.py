"""
This is the main file of a library app.
It contains the main class and main functions.
"""
from PyQt6.QtWidgets import QApplication, QMainWindow
from sqlconnector import create_connection
import os, sys

class LibraryApp(QMainWindow):
    def __init__(self) -> None:
      super().__init__()
      
      self.initUi()
      
    def initUi(self) -> None:
        raise NotImplementedError("initUi method is not implemented yet")
    
    
if __name__ == "__main__":
    app = QApplication([])

    if not create_connection('QSQLITE'):
        sys.exit(1)

    window = LibraryApp()
    window.show()

    app.exec()