import json
import re
import tkinter as tk
import os
from tkinter import messagebox



#PART 4 

import sqlite3
import shutil

class SchoolDatabase:
    def __init__(self, db_name="school.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS instructors (
            instructor_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            instructor_id TEXT,
            FOREIGN KEY (instructor_id) REFERENCES instructors (instructor_id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            student_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (student_id),
            FOREIGN KEY (course_id) REFERENCES courses (course_id),
            PRIMARY KEY (student_id, course_id)
        )
        ''')

        self.conn.commit()

    def close(self):
        self.conn.close()

    def create_record(db_file, table_name, columns, values):
    
        try:
            
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            placeholders = ', '.join('?' * len(values))
            sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            cursor.execute(sql, values)
            
            conn.commit()
            
            conn.close()
            print("Record inserted successfully.")
        
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def read_records(db_file, table_name):
   
        try:
           
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()

            sql = f"SELECT * FROM {table_name}"
            
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            
            conn.close()
            
        
            print('\n')
            print(table_name)
            print('\n')
            print(rows)
            print('\n')
    
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []


    def update_record(db_file, table_name, update_values, condition):
       
        try:

            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            set_clause = ', '.join([f"{col} = ?" for col in update_values.keys()])
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"

            cursor.execute(sql, list(update_values.values()))
            
            conn.commit()
            
            conn.close()
            print("Record updated successfully.")
        
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")


    def delete_record(db_file, table_name, condition):
      
        try:
         
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
        
            sql = f"DELETE FROM {table_name} WHERE {condition}"
            
            cursor.execute(sql)
            
            conn.commit()
            
            conn.close()
            print("Record deleted successfully.")
        
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

   
    def backup_database(db_file, backup_file):
        try:
            
            shutil.copy2(db_file, backup_file)
            print(f"Backup successful: {backup_file}")
        except IOError as e:
            print(f"An error occurred while backing up the database: {e}")






#PART 1 


def validate_email(email):
    email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    if not re.match(email_regex, email):
        raise ValueError(f"Please enter a valid email address: {email}")

def validate_non_empty_string(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is mandatory.")

def validate_age(age):
    if not isinstance(age, int) or age < 0:
        raise ValueError("Age cannot be negative.")

class Person:
    def __init__(self, name: str, age: int, email: str):
        validate_non_empty_string(name, "Name")
        validate_age(age)
        validate_email(email)

        self.name = name
        self.age = age
        self._email = email

    def introduce(self):
        print(f"Hi, my name is {self.name} and I'm {self.age} years old.")

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "email": self._email
        }

    def save(self, file):
        with open(file, 'w') as f:
            json.dump(self.to_dict(), f)

    @classmethod
    def load(cls, file):
        with open(file, 'r') as f:
            data = json.load(f)
        return cls(data['name'], data['age'], data['email'])

class Student(Person):
    def __init__(self, name: str, age: int, email: str, student_id: str):
        super().__init__(name, age, email)
        validate_non_empty_string(student_id, "Student ID")
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        if course.id not in self.registered_courses:
            self.registered_courses.append(course.id)  
            course.enrolled_students.append(self.student_id)
            course.save('course_data.json')
            self.save('student_data.json')
            print(f"{self.name} has registered for {course.name}")
        else:
            print(f"{self.name} is already registered for {course.name}")

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "email": self._email,
            "student_id": self.student_id,
            "registered_courses": [course for course in self.registered_courses]
        }

    @classmethod
    def load(cls, file,id):
        with open(file, 'r') as f:
            students = json.load(f)
        return Student(students[id]['name'], students[id]['age'], students[id]['email'], id)
    
    def save(self, file):

        with open(file, 'r') as f:

            file_content = f.read()
            if file_content.strip():  
                students= json.loads(file_content)
            else:
                students = {}  

        students[self.student_id] = self.to_dict()

        with open(file, 'w') as f:
            json.dump(students, f, indent=4)

    @classmethod
    def load_all(cls, file):
        try:
            with open(file, 'r') as f:
                students_data = json.load(f)
            return students_data
        except (FileNotFoundError, json.JSONDecodeError):
            return []


class Instructor(Person):

    def __init__(self, name: str, age: int, email: str, instructor_id: str):
        super().__init__(name, age, email)
        validate_non_empty_string(instructor_id, "Instructor ID")
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        if course.id not in self.assigned_courses:
            self.assigned_courses.append(course)
            course.instructor = self
           
            course.save('course_data.json')
            self.save('instructor_data.json')
            print(f"Instructor {self.name} has been assigned to course {course.name}")
        else:
            print(f"Instructor {self.name} is already assigned to course {course.name}")

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "email": self._email,
            "instructor_id": self.instructor_id,
            "assigned_courses": [course.id for course in self.assigned_courses]
        }


    def save(self, file):

     
        with open(file, 'r') as f:
        
            file_content = f.read()
            if file_content.strip():  
                instructors = json.loads(file_content)
            else:
                instructors = {}  



        if not isinstance(instructors, dict):
            raise ValueError("Data in file is not a dictionary")

    
        instructors[self.instructor_id] = self.to_dict()

        with open(file, 'w') as f:
            json.dump(instructors, f, indent=4)

    @classmethod
    def load_all(cls, file):
        try:
            with open(file, 'r') as f:
                instructors_data = json.load(f)
            return instructors_data
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
    @classmethod
    def load(cls, file,id):
        with open(file, 'r') as f:
            instructors = json.load(f)
        print(id)
  
        return Instructor(instructors[id]['name'], instructors[id]['age'], instructors[id]['email'], id)

class Course:
    def __init__(self, id: str, name: str, instructor: Instructor):
        validate_non_empty_string(id, "Course ID")
        validate_non_empty_string(name, "Course Name")
        self.id = id
        self.name = name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student: Student):
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)
            print(f"{student.name} has been added to the course: {self.name}")
        else:
            print(f"{student.name} is already enrolled in the course: {self.name}")

    def to_dict(self):

        if (self.instructor is not None):
     
            return {
                "id": self.id,
                "name": self.name,
                "instructor": self.instructor.to_dict(),
                "enrolled_students": [student for student in self.enrolled_students]
            }
        
        else:
            return {
                "id": self.id,
                "name": self.name,
                "instructor":None,
                "enrolled_students": [student for student in self.enrolled_students]
            }

    def save(self, file):

        with open(file, 'r') as f:

            file_content = f.read()
            if file_content.strip():  
                courses= json.loads(file_content)
            else:
                courses = {}  

        courses[self.id] = self.to_dict()

        with open(file, 'w') as f:
            json.dump(courses, f, indent=4)

    @classmethod
    def load(cls, file,id):
        with open(file, 'r') as f:
            courses = json.load(f)
        if courses[id]['instructor'] is None:
            return Course(courses[id]['id'], courses[id]['name'], None)
        
        instructor =Instructor.load('instructor_data.json',courses[id]['instructor']['instructor_id'])

        return Course(id, courses[id]['name'], instructor)

    @classmethod
    def load_all(cls, file):
        try:
            with open(file, 'r') as f:
                courses_data = json.load(f)
         
            return courses_data
        except (FileNotFoundError, json.JSONDecodeError):
            return []

# PART 3

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, 
                             QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QComboBox, QFormLayout, QTableWidget, QTableWidgetItem, QFileDialog,
                             QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
import json
import os
import csv

class SchoolManagementSystem(QMainWindow):
    """
    Main class for the School Management System GUI application. 
    Handles student, instructor, and course management including adding, 
    deleting, and editing records, as well as course registration.
    """
    def __init__(self):
        """
        Initializes the School Management System application.
        Sets up the window, loads data, and creates the UI tabs.
        """
        super().__init__()

        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)

     
        self.students = {}
        self.instructors = {}
        self.courses = {}

       
        if os.path.exists('student_data.json'):
            self.students = self.load_data('student_data.json')
        else:
            self.save_data('student_data.json', self.students)

        if os.path.exists('instructor_data.json'):
            self.instructors = self.load_data('instructor_data.json')
        else:
            self.save_data('instructor_data.json', self.instructors)

        if os.path.exists('course_data.json'):
            self.courses = self.load_data('course_data.json')
        else:
            self.save_data('course_data.json', self.courses)

        self.course_var = ""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.create_student_tab()
        self.create_instructor_tab()
        self.create_course_tab()
        self.create_display_tab()

    def create_display_tab(self):
        """
        Creates the 'Records' tab for viewing, searching, editing, and exporting records.
        """
        records_tab = QWidget()
        self.tabs.addTab(records_tab, "Records")

        layout = QVBoxLayout(records_tab)

        search_layout = QVBoxLayout()
        layout.addLayout(search_layout)

        search_label = QLabel("Search:")
        search_layout.addWidget(search_label)

        self.search_var = QLineEdit()
        search_layout.addWidget(self.search_var)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_records)
        search_layout.addWidget(search_button)

        self.records_table = QTableWidget()
        self.records_table.setColumnCount(4)
        self.records_table.setHorizontalHeaderLabels(["ID", "Name", "Type", "Additional Info"])
        self.records_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.records_table)

        button_layout = QVBoxLayout()
        layout.addLayout(button_layout)

        self.edit_button = QPushButton("Edit Record")
        self.edit_button.clicked.connect(self.edit_record)
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Record")
        self.delete_button.clicked.connect(self.delete_record)
        button_layout.addWidget(self.delete_button)

        self.export_button = QPushButton("Export to CSV")
        self.export_button.clicked.connect(self.export_to_csv)
        layout.addWidget(self.export_button)

        self.load_all_records()

    def export_to_csv(self):
        """
        Exports the current records to a CSV file selected by the user.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if not file_path:
            return

        if not file_path.endswith('.csv'):
            file_path += '.csv'

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                
                headers = [self.records_table.horizontalHeaderItem(i).text() for i in range(self.records_table.columnCount())]
                writer.writerow(headers)

                
                for row in range(self.records_table.rowCount()):
                    row_data = []
                    for column in range(self.records_table.columnCount()):
                        item = self.records_table.item(row, column)
                        row_data.append(item.text() if item is not None else "")
                    writer.writerow(row_data)

            QMessageBox.information(self, "Export Successful", f"Records have been successfully exported to {file_path}.")

        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Failed to export records: {str(e)}")

    def load_all_records(self):
        """
        Loads all records (students, instructors, courses) into the table for display.
        """
        self.records_table.setRowCount(0)  

  
        for student_id, student_data in self.students.items():
            name = student_data.get('name', 'N/A')
            age = student_data.get('age', 'N/A')
            email = student_data.get('email', 'N/A')
            row_position = self.records_table.rowCount()
            self.records_table.insertRow(row_position)
            self.records_table.setItem(row_position, 0, QTableWidgetItem(student_id))
            self.records_table.setItem(row_position, 1, QTableWidgetItem(name))
            self.records_table.setItem(row_position, 2, QTableWidgetItem("Student"))
            self.records_table.setItem(row_position, 3, QTableWidgetItem(f"Age: {age}, Email: {email}"))

   
        for instructor_id, instructor_data in self.instructors.items():
            name = instructor_data.get('name', 'N/A')
            age = instructor_data.get('age', 'N/A')
            email = instructor_data.get('email', 'N/A')
            row_position = self.records_table.rowCount()
            self.records_table.insertRow(row_position)
            self.records_table.setItem(row_position, 0, QTableWidgetItem(instructor_id))
            self.records_table.setItem(row_position, 1, QTableWidgetItem(name))
            self.records_table.setItem(row_position, 2, QTableWidgetItem("Instructor"))
            self.records_table.setItem(row_position, 3, QTableWidgetItem(f"Age: {age}, Email: {email}"))


        for course_id, course_data in self.courses.items():
            course_name = course_data.get('name', 'N/A')
            instructor_info = course_data['instructor']
            instructor_details = "Instructor: N/A" if not instructor_info else f"Instructor: {instructor_info['name']}"
            row_position = self.records_table.rowCount()
            self.records_table.insertRow(row_position)
            self.records_table.setItem(row_position, 0, QTableWidgetItem(course_id))
            self.records_table.setItem(row_position, 1, QTableWidgetItem(course_name))
            self.records_table.setItem(row_position, 2, QTableWidgetItem("Course"))
            self.records_table.setItem(row_position, 3, QTableWidgetItem(instructor_details))

    def edit_record(self):
        """
        Allows the user to edit a selected record from the table.
        """
        selected_row = self.records_table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Edit Record", "Please select a record to edit.")
            return

        record_id = self.records_table.item(selected_row, 0).text()
        record_type = self.records_table.item(selected_row, 2).text()

       
        for column in range(self.records_table.columnCount()):
            self.records_table.item(selected_row, column).setFlags(self.records_table.item(selected_row, column).flags() | Qt.ItemIsEditable)

        self.records_table.itemChanged.connect(lambda item: self.save_record(item, record_id, record_type))
        QMessageBox.information(self, "Edit Record", "You can now edit the selected record. Don't forget to save the changes!")

    def save_record(self, item, record_id, record_type):
        """
        Saves changes made to a record after editing.
        """
        row = item.row()
        column = item.column()
        new_value = item.text()

        if record_type == "Student":
            if column == 1:  
                self.students[record_id]['name'] = new_value
            elif column == 3: 
                age = int(new_value.split(",")[0].split(":")[1].strip())
                self.students[record_id]['age'] = age
            elif column == 3:  
                email = new_value.split(",")[1].split(":")[1].strip()
                self.students[record_id]['email'] = email
            json.dump(self.students, open('student_data.json', 'w'))

        elif record_type == "Instructor":
            if column == 1:  
                self.instructors[record_id]['name'] = new_value
            elif column == 3:  
                age = int(new_value.split(",")[0].split(":")[1].strip())
                self.instructors[record_id]['age'] = age
            elif column == 3: 
                email = new_value.split(",")[1].split(":")[1].strip()
                self.instructors[record_id]['email'] = email
            json.dump(self.instructors, open('instructor_data.json', 'w'))

        elif record_type == "Course":
            if column == 1:  
                self.courses[record_id]['name'] = new_value
            elif column == 3:  
                instructor_name = new_value.split(":")[1].strip()
                self.courses[record_id]['instructor']['name'] = instructor_name
            json.dump(self.courses, open('course_data.json', 'w'))

        QMessageBox.information(self, "Save Record", "The changes have been saved successfully.")

    def delete_record(self):
        """
        Deletes the selected record from the records table and the corresponding JSON file.
        If the record is of type "Student", "Instructor", or "Course", it is removed from the respective dictionary 
        and the updated data is saved back to the corresponding JSON file.
        """
        selected_row = self.records_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Delete Record", "Please select a record to delete.")
            return

        record_id = self.records_table.item(selected_row, 0).text()
        record_type = self.records_table.item(selected_row, 2).text()

        if record_type == "Student" and record_id in self.students:
            del self.students[record_id]
            json.dump(self.students, open('student_data.json', 'w'))

        elif record_type == "Instructor" and record_id in self.instructors:
            del self.instructors[record_id]
            json.dump(self.instructors, open('instructor_data.json', 'w'))

        elif record_type == "Course" and record_id in self.courses:
            del self.courses[record_id]
            json.dump(self.courses, open('course_data.json', 'w'))

        self.records_table.removeRow(selected_row)
        self.load_all_records()
        QMessageBox.information(self, "Delete Record", "Record deleted successfully.")

    def create_student_tab(self):
        """
        Creates and sets up the Student tab in the GUI, which allows the user to add a new student 
        and register them for a course.
        """
        student_tab = QWidget()
        self.tabs.addTab(student_tab, "Student")

        layout = QFormLayout(student_tab)
        
        self.student_name = QLineEdit()
        self.student_age = QLineEdit()
        self.student_email = QLineEdit()
        self.student_id = QLineEdit()

        layout.addRow(QLabel("Name:"), self.student_name)
        layout.addRow(QLabel("Age:"), self.student_age)
        layout.addRow(QLabel("Email:"), self.student_email)
        layout.addRow(QLabel("Student ID:"), self.student_id)

        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student)
        layout.addWidget(add_student_button)

        self.student_course_dropdown = QComboBox()
        self.update_student_course_dropdown()
        layout.addRow(QLabel("Register for Course:"), self.student_course_dropdown)

        register_course_button = QPushButton("Register for Course")
        register_course_button.clicked.connect(self.register_course)
        layout.addWidget(register_course_button)

    def search_records(self):
        """
        Searches for records in the table that match the search query and hides rows that do not match.
        """
        search_query = self.search_var.text().lower()

        for row in range(self.records_table.rowCount()):
            match_found = False
            for column in range(self.records_table.columnCount()):
                item = self.records_table.item(row, column)
                if search_query in item.text().lower():
                    match_found = True
                    break
            self.records_table.setRowHidden(row, not match_found)

    def create_instructor_tab(self):
        """
        Creates and sets up the Instructor tab in the GUI, which allows the user to add a new instructor 
        and assign them to a course.
        """
        instructor_tab = QWidget()
        self.tabs.addTab(instructor_tab, "Instructor")

        layout = QFormLayout(instructor_tab)
        
        self.instructor_name = QLineEdit()
        self.instructor_age = QLineEdit()
        self.instructor_email = QLineEdit()
        self.instructor_id = QLineEdit()

        layout.addRow(QLabel("Name:"), self.instructor_name)
        layout.addRow(QLabel("Age:"), self.instructor_age)
        layout.addRow(QLabel("Email:"), self.instructor_email)
        layout.addRow(QLabel("Instructor ID:"), self.instructor_id)

        add_instructor_button = QPushButton("Add Instructor")
        add_instructor_button.clicked.connect(self.add_instructor)
        layout.addWidget(add_instructor_button)
        
        self.instructor_course_dropdown = QComboBox()
        self.update_instructor_course_dropdown()
        layout.addRow(QLabel("Assign to Course:"), self.instructor_course_dropdown)

        assign_course_button = QPushButton("Assign to Course")
        assign_course_button.clicked.connect(self.assign_course)
        layout.addWidget(assign_course_button)

    def create_course_tab(self):
        """
        Creates and sets up the Course tab in the GUI, which allows the user to add a new course 
        and associate it with an instructor.
        """
        course_tab = QWidget()
        self.tabs.addTab(course_tab, "Course")

        layout = QFormLayout(course_tab)

        self.course_name = QLineEdit()
        self.course_id = QLineEdit()
        self.course_instructor_id = QLineEdit()

        layout.addRow(QLabel("Course Name:"), self.course_name)
        layout.addRow(QLabel("Course ID:"), self.course_id)
        layout.addRow(QLabel("Instructor ID:"), self.course_instructor_id)

        add_course_button = QPushButton("Add Course")
        add_course_button.clicked.connect(self.add_course)
        layout.addWidget(add_course_button)

    def load_data(self, filename):
        """
        Loads and returns the data from the specified JSON file.
        """
        with open(filename, 'r') as file:
            return json.load(file)

    def save_data(self, filename, data):
        """
        Saves the provided data to the specified JSON file.
        """
        with open(filename, 'w') as file:
            json.dump(data, file)

    def add_student(self):
        """
        Adds a new student to the system based on the form input fields. 
        Saves the student data to the JSON file and database, then clears the input fields.
        """
        student_id = self.student_id.text()
        student = {
            'name': self.student_name.text(),
            'age': int(self.student_age.text()),
            'email': self.student_email.text(),
            'student_id': self.student_id.text(),
        }

        self.students[student_id] = student
        self.save_data('student_data.json', self.students)
        self.student_name.clear()
        self.student_age.clear()
        self.student_email.clear()
        self.student_id.clear()
        self.update_student_course_dropdown()

        columns = ['student_id', 'name', 'age', 'email']
        values = [student_id, student['name'], student['age'], student['email']]
        SchoolDatabase.create_record('school.db', 'students', columns, values)
        self.load_all_records()

    def add_instructor(self):
        """
        Adds a new instructor to the system based on the form input fields. 
        Saves the instructor data to the JSON file and database, then clears the input fields.
        """
        instructor_id = self.instructor_id.text()
        instructor = {
            'name': self.instructor_name.text(),
            'age': int(self.instructor_age.text()),
            'email': self.instructor_email.text(),
            'instructor_id': self.instructor_id.text()
        }
        self.instructors[instructor_id] = instructor
        self.save_data('instructor_data.json', self.instructors)
        self.instructor_name.clear()
        self.instructor_age.clear()
        self.instructor_email.clear()
        self.instructor_id.clear()
        self.update_instructor_course_dropdown()

        columns = ['instructor_id', 'name', 'age', 'email']
        values = [instructor_id, instructor['name'], instructor['age'], instructor['email']]
        SchoolDatabase.create_record('school.db', 'instructors', columns, values)
        self.load_all_records()

    def add_course(self):
        """
        Adds a new course to the system based on the form input fields. 
        Saves the course data to the JSON file and database, then clears the input fields.
        """
        course_id = self.course_id.text()
        instructor_id = self.course_instructor_id.text()
        instructor = self.instructors.get(instructor_id, None)

        course = {
            'id': course_id,    
            'name': self.course_name.text(),
            'instructor': instructor
        }

        self.courses[course_id] = course
        self.save_data('course_data.json', self.courses)
        self.course_name.clear()
        self.course_id.clear()
        self.course_instructor_id.clear()
        self.update_student_course_dropdown()
        self.update_instructor_course_dropdown()

        columns = ['course_id', 'name', 'instructor_id']
        values = [course_id, self.course_name.text(), instructor_id]
        SchoolDatabase.create_record('school.db', 'courses', columns, values)
        self.load_all_records()

    def update_student_course_dropdown(self):
        """
        Updates the course dropdown for the Student tab with the list of available courses.
        """
        self.student_course_dropdown.clear()
        self.student_course_dropdown.addItems(list(self.courses.keys()))

    def update_instructor_course_dropdown(self):
        """
        Updates the course dropdown for the Instructor tab with the list of courses without assigned instructors.
        """
        self.instructor_course_dropdown.clear()
        empty_instructor_course_ids = [course_id for course_id, course in self.courses.items() if not course.get('instructor')]
        self.instructor_course_dropdown.addItems(empty_instructor_course_ids)

    def register_course(self):
        """
        Registers the student for the selected course and updates the course registration in the database.
        """
        student_id = self.student_id.text()
        course_id = self.student_course_dropdown.currentText()

        if student_id not in self.students.keys():
            self.show_error_message("Student Not Found", "The selected student ID is not found in the system.")
            return

        registration_data = {
            'student_id': student_id,
            'course_id': course_id
        }

        SchoolDatabase.create_record('school.db', 'registrations', list(registration_data.keys()), list(registration_data.values()))
        self.load_all_records()

    def assign_course(self):
        """
        Assigns the instructor to the selected course and updates the course assignment in the database.
        """
        instructor_id = self.instructor_id.text()
        course_id = self.instructor_course_dropdown.currentText()

        if instructor_id not in self.instructors.keys():
            self.show_error_message("Instructor Not Found", "The selected instructor ID is not found in the system.")
            return

        self.courses[course_id]['instructor'] = self.instructors[instructor_id]
        self.save_data('course_data.json', self.courses)
        self.update_instructor_course_dropdown()

        SchoolDatabase.update_record('school.db', 'courses', ['instructor_id'], [instructor_id], 'course_id', course_id)
        self.load_all_records()


    def show_error_message(self, title, message):
        """
        Displays an error message dialog box with the specified title and message.

        Args:
            title (str): The title of the error message box.
            message (str): The content of the error message.
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.exec_()






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    db=SchoolDatabase()
    # SchoolDatabase.read_records('school.db', 'students')
    # SchoolDatabase.read_records('school.db', 'instructors')
    # SchoolDatabase.read_records('school.db', 'courses')
    # SchoolDatabase.read_records('school.db', 'registrations')
    sys.exit(app.exec_())