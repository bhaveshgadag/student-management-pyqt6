import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QLineEdit, \
    QComboBox, QPushButton, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        # File Menu
        file_menu = self.menuBar().addMenu("&File")
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu.addAction(add_student_action)

        # Edit Menu
        edit_menu = self.menuBar().addMenu("Edit")
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu.addAction(search_action)
        search_action.triggered.connect(self.search)

        # Help Menu
        help_menu = self.menuBar().addMenu("&Help")
        help_action = QAction("About", self)
        help_menu.addAction(help_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Toolbar
        self.toolbar = QToolBar()
        self.toolbar.setMovable(True)
        self.addToolBar(self.toolbar)
        self.toolbar.addAction(add_student_action)
        self.toolbar.addAction(search_action)

        # Statusbar
        edit_button = QPushButton("Edit record")
        delete_button = QPushButton("Delete record")
        self.statusBar().addWidget(edit_button)
        self.statusBar().addWidget(delete_button)
        edit_button.clicked.connect(self.edit_record)

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

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit_record(self):
        dialog = EditDialog()
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


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Search Students")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # student name
        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        # search button
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.name.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE NAME = ?", (name,))
        result = list(result)
        items = main_win.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        print(items)
        for item in items:
            print(item)
            main_win.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit student record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        index = main_win.table.currentIndex()
        student_name = main_win.table.item(index, 1).text()
        print(student_name)

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

app = QApplication(sys.argv)
main_win = MainWindow()
main_win.show()
main_win.load_data()
sys.exit(app.exec())
