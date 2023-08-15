import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QAction
import sqlite3


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

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("Select * from students")
        data = cursor.fetchall()
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(data):
            self.table.insertRow(row_number)
            for column_no, data in enumerate(row_data):
                self.table.setItem(row_number, column_no, QTableWidgetItem(str(data)))
        connection.close()


app = QApplication(sys.argv)
main_win = MainWindow()
main_win.show()
main_win.load_data()
sys.exit(app.exec())
