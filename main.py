import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QLineEdit, \
    QComboBox, QPushButton, QToolBar, QStatusBar, QLabel, QGridLayout, QMessageBox
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sqlite3
import mysql.connector


class Database():
    def __init__(self, host='localhost', user='root', password='root', database='school'):
        self.host= host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        connection = mysql.connector.connect(self.host, self.user, self.password, self.database)
        return connection


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
        about_action = QAction("About", self)
        help_menu.addAction(about_action)
        about_action.triggered.connect(self.about)

        # Main table of student records
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
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.table.cellClicked.connect(self.cell_clicked)

    # Add buttons to status bar on cell click
    def cell_clicked(self):
        # Remove previously added buttons to status bar
        children = main_win.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusBar.removeWidget(child)

        # Add edit and delete to statusbar
        edit_button = QPushButton("Edit record")
        delete_button = QPushButton("Delete record")
        self.statusBar.addWidget(edit_button)
        self.statusBar.addWidget(delete_button)
        edit_button.clicked.connect(self.edit_record)
        delete_button.clicked.connect(self.delete_record)

    # Function to load student records in main table
    def load_data(self):
        connection = Database().connect()
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

    # Initialize Insert Dialog
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    # Initialize Search Dialog
    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    # Initialize Edit Dialog
    def edit_record(self):
        dialog = EditDialog()
        dialog.exec()

    # Initialize Delete Dialog
    def delete_record(self):
        dialog = DeleteDialog()
        dialog.exec()

    # Initialize About Dialog
    def about(self):
        dialog = AboutDialog()
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

    # Function to insert new Student record in DB
    def insert_record(self):
        student = self.student.text()
        course = self.course_cb.itemText(self.course_cb.currentIndex())
        mobile = self.mobile.text()

        connection = Database().connect()
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

        # Student name
        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        # search button
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    # Function to search student record in DB for entered input
    def search(self):
        name = self.name.text()

        connection = Database().connect()
        cursor = connection.cursor()
        result = cursor.execute("SELECT id FROM students WHERE name = ?", (name,))
        print(result)
        print(result.fetchall())
        # result = list(result)
        items = main_win.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_win.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit student record")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        row = main_win.table.currentRow()
        student_name = main_win.table.item(row, 1).text()
        course = main_win.table.item(row, 2).text()
        mobile = main_win.table.item(row, 3).text()
        print(student_name)

        layout = QVBoxLayout()

        # Student name input
        self.student = QLineEdit(student_name)
        self.student.setPlaceholderText("Name")
        layout.addWidget(self.student)

        # Course input
        self.course_cb = QComboBox()
        courses = ["Biology", "Astronomy", "Math", "Physics"]
        self.course_cb.addItems(courses)
        layout.addWidget(self.course_cb)
        self.course_cb.setCurrentText(course)

        # Mobile input
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Submit button
        button = QPushButton("Update")
        layout.addWidget(button)
        button.clicked.connect(self.update_record)

        self.setLayout(layout)

    def update_record(self):
        student = self.student.text()
        course = self.course_cb.itemText(self.course_cb.currentIndex())
        mobile = self.mobile.text()
        index = main_win.table.currentRow()
        s_id = main_win.table.item(index, 0).text()

        connection = Database().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name=?, course=?, mobile=? WHERE id=?",
                       (student, course, mobile, s_id))
        connection.commit()
        cursor.close()
        connection.close()
        main_win.load_data()
        main_win.table.setCurrentCell(index, 0)


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Record")

        layout = QGridLayout()
        msg = QLabel("Are you sure you want to delete this record?")
        layout.addWidget(msg, 0, 0, 1, 2)

        yes = QPushButton('Yes')
        no = QPushButton('no')
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)

        yes.clicked.connect(self.delete_record)
        no.clicked.connect(self.close)

        self.setLayout(layout)

    def delete_record(self):
        index = main_win.table.currentRow()
        s_id = main_win.table.item(index, 0).text()

        connection = Database().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students where id=?", (s_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_win.load_data()
        self.close()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About")
        content = '''
        Student Management System
        Created by Bhavesh
        
        This is a simple student management application 
        developed using Python, PyQt6 for GUI and 
        sqlite3 for storing records.
        '''
        self.setText(content)

        # self.setLayout(layout)


app = QApplication(sys.argv)
main_win = MainWindow()
main_win.show()
main_win.load_data()
sys.exit(app.exec())
