from PyQt6.QtWidgets import QApplication, QDialog, QFormLayout
import sys

class SaveResultDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

if __name__ == "__main__":
    app = QApplication([])
    dialog = SaveResultDialog()
    dialog.exec()
    sys.exit(1)
    app.exec()