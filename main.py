import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        help_action = QAction("About", self)

        file_menu.addAction(add_student_action)
        help_menu.addAction(help_action)


app = QApplication(sys.argv)
main_win = MainWindow()
main_win.show()
sys.exit(app.exec())
