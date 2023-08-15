import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QLineEdit, \
    QComboBox, QPushButton
from PyQt6.QtGui import QAction
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
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
        cursor.close()
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add student record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Student name input
        self.student = QLineEdit()
        self.student.setPlaceholderText("Name")
        layout.addWidget(self.student)

        # Course input
        self.course_cb = QComboBox()
        courses = ["Biology", "Astronomy", "Math", "Physics"]
        self.course_cb.addItems(courses)
        layout.addWidget(self.course_cb)

        # Mobile input
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Submit button
        button = QPushButton("Add")
        button.clicked.connect(self.insert_record)
        layout.addWidget(button)

        self.setLayout(layout)

    def insert_record(self):
        student = self.student.text()
        course = self.course_cb.itemText(self.course_cb.currentIndex())
        mobile = self.mobile.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ? , ?)",
                       (student, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_win.load_data()


app = QApplication(sys.argv)
main_win = MainWindow()
main_win.show()
main_win.load_data()
sys.exit(app.exec())
