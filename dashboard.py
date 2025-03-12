from PyQt6.QtWidgets import QApplication, QDialog, QFormLayout

class DashboardDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

if __name__ == "__main__":
    app = QApplication([])
    dialog = DashboardDialog()
    dialog.exec()
    app.exec()