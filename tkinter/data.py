import sqlite3

def create_database():
    connection = sqlite3.connect('school_management_system.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL UNIQUE,
        student_id TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS instructors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL UNIQUE,
        instructor_id TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id TEXT NOT NULL UNIQUE,
        course_name TEXT NOT NULL,
        instructor_id INTEGER,
        FOREIGN KEY (instructor_id) REFERENCES instructors (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registrations (
        student_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (course_id) REFERENCES courses (id),
        PRIMARY KEY (student_id, course_id) 
    )
    ''')

    connection.commit()
    connection.close()

#create_database()

from typing import List

def execute_query(query: str, parameters: tuple = ()):
    connection = sqlite3.connect('school_management_system.db')
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    connection.commit()
    connection.close()

def fetch_query(query: str, parameters: tuple = ()) -> List[tuple]:
    connection = sqlite3.connect('school_management_system.db')
    cursor = connection.cursor()
    cursor.execute(query, parameters)
    results = cursor.fetchall()
    connection.close()
    return results

def add_student(name, age, email, student_id):
    conn = sqlite3.connect('school_management_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (student_id, name, age, email) VALUES (?, ?, ?, ?)
    ''', (student_id, name, age, email))
    conn.commit()
    conn.close()

def add_instructor(name, age, email, instructor_id):
    conn = sqlite3.connect('school_management_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Instructors (instructor_id, name, age, email) VALUES (?, ?, ?, ?)
    ''', (instructor_id, name, age, email))
    conn.commit()
    conn.close()

def add_course(course_id, name, instructor_name):
    conn = sqlite3.connect('school_management_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Courses (course_id, name, instructor_name) VALUES (?, ?, ?)
    ''', (course_id, name, instructor_name))
    conn.commit()
    conn.close()

def register_student_to_course(student_name, course_name):
    conn = sqlite3.connect('school_management_system.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name FROM Students WHERE name = ?
    ''', (student_name,))
    student = cursor.fetchone()
    
    cursor.execute('''
        SELECT name FROM Courses WHERE name = ?
    ''', (course_name,))
    course = cursor.fetchone()

    if student and course:
        cursor.execute('''
            INSERT INTO Registrations (student_name, course_name) VALUES (?, ?)
        ''', (student_name, course_name))
        conn.commit()
    else:
        raise ValueError("Student or course not found.")

    conn.close()

def get_all_students():
    conn = sqlite3.connect('school_management_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Students')
    students = cursor.fetchall()
    conn.close()
    return students

def get_all_instructors():
    conn = sqlite3.connect('school_management_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Instructors')
    instructors = cursor.fetchall()
    conn.close()
    return instructors

def get_all_courses():
    conn = sqlite3.connect('school_management_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Courses')
    courses = cursor.fetchall()
    conn.close()
    return courses

def update_student(student_id: int, name: str, age: int, email: str):
    execute_query('''
    UPDATE students SET name = ?, age = ?, email = ? WHERE id = ?
    ''', (name, age, email, student_id))

def delete_student(student_id: int):
    execute_query('DELETE FROM students WHERE id = ?', (student_id,))

import shutil

def backup_database():
    shutil.copy('school_management_system.db', 'backup_school_management_system.db')
