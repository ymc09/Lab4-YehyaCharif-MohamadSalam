import re
import json
import os
from typing import List, Dict, Any
import data as data

def is_valid_email(email: str) -> bool:
    """
    Check if the provided email is in a valid format.

    :param email: The email address to validate.
    :type email: str
    :return: True if the email is valid, False otherwise.
    :rtype: bool
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_non_negative_age(age: int) -> bool:
    """
    Check if the provided age is non-negative.

    :param age: The age to validate.
    :type age: int
    :return: True if the age is non-negative, False otherwise.
    :rtype: bool
    """
    return age >= 0

class Person:
    """
    A class representing a person with basic attributes like name, age, and email.
    """
    def __init__(self, name: str, age: int, email: str):
        """
        Initialize a new instance of the Person class.

        :param name: The name of the person.
        :type name: str
        :param age: The age of the person.
        :type age: int
        :param email: The email of the person.
        :type email: str
        :raises ValueError: If the age is negative or the email is invalid.
        """
        if not is_non_negative_age(age):
            raise ValueError("Age must be non-negative.")
        if not is_valid_email(email):
            raise ValueError("Invalid email format.")
        self.name = name
        self.age = age
        self._email = email 

    def introduce(self):
        """
        Print an introduction message with the person's name and age.
        """
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the person object to a dictionary.

        :return: A dictionary representation of the person.
        :rtype: dict
        """
        return {
            'name': self.name,
            'age': self.age,
            'email': self._email
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Person':
        """
        Create a Person object from a dictionary.

        :param data: A dictionary containing person data.
        :type data: dict
        :return: A Person instance created from the dictionary.
        :rtype: Person
        """
        return Person(
            name=data['name'],
            age=data['age'],
            email=data['email']
        )
    
    def save_to_file(self, filename: str):
        """
        Save the person object to a file in JSON format.

        :param filename: The file path where the object will be saved.
        :type filename: str
        """
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file, indent=4)
    
    @staticmethod
    def load_from_file(filename: str) -> 'Person':
        """
        Load a Person object from a file in JSON format.

        :param filename: The file path to load the person from.
        :type filename: str
        :return: A Person instance created from the file.
        :rtype: Person
        """
        with open(filename, 'r') as file:
            data = json.load(file)
            return Person.from_dict(data)

class Student(Person):
    """
    A class representing a student, inheriting from Person.
    """
    def __init__(self, name: str, age: int, email: str, student_id: str, registered_courses: List['Course']):
        """
        Initialize a new instance of the Student class.

        :param name: The name of the student.
        :type name: str
        :param age: The age of the student.
        :type age: int
        :param email: The email of the student.
        :type email: str
        :param student_id: The ID of the student.
        :type student_id: str
        :param registered_courses: A list of registered courses for the student.
        :type registered_courses: list
        """
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = registered_courses if registered_courses is not None else []

    def register_course(self, course: 'Course'):
        """
        Register the student for a new course.

        :param course: The course to register the student for.
        :type course: Course
        """
        if course not in self.registered_courses:
            self.registered_courses.append(course)
            course.add_student(self)  
            print(f"Student '{self.name}' has been registered for course '{course.course_name}'.")
        else:
            print(f"Student {self.name} is already registered for {course.course_name}.")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the student object to a dictionary.

        :return: A dictionary representation of the student.
        :rtype: dict
        """
        data = super().to_dict()
        data.update({
            'student_id': self.student_id,
            'registered_courses': [course.course_id for course in self.registered_courses]  
        })
        return data
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Student':
        """
        Create a Student object from a dictionary.

        :param data: A dictionary containing student data.
        :type data: dict
        :return: A Student instance created from the dictionary.
        :rtype: Student
        """
        registered_courses = [Course.from_dict(course) for course in data.get('registered_courses', [])]
        return Student(
            name=data['name'],
            age=data['age'],
            email=data['email'],
            student_id=data['student_id'],
            registered_courses=registered_courses
        )

class Instructor(Person):
    """
    A class representing an instructor, inheriting from Person.
    """
    def __init__(self, name: str, age: int, email: str, instructor_id: str, assigned_courses: List['Course']):
        """
        Initialize a new instance of the Instructor class.

        :param name: The name of the instructor.
        :type name: str
        :param age: The age of the instructor.
        :type age: int
        :param email: The email of the instructor.
        :type email: str
        :param instructor_id: The ID of the instructor.
        :type instructor_id: str
        :param assigned_courses: A list of assigned courses for the instructor.
        :type assigned_courses: list
        """
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses if assigned_courses is not None else []

    def assign_course(self, course: 'Course'):
        """
        Assign the instructor to a new course.

        :param course: The course to assign the instructor to.
        :type course: Course
        """
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
            print(f"Instructor '{self.name}' has been assigned to course '{course.course_name}'.")
        else:
            print(f"Instructor {self.name} is already assigned to {course.course_name}.")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the instructor object to a dictionary.

        :return: A dictionary representation of the instructor.
        :rtype: dict
        """
        data = super().to_dict()
        data.update({
            'instructor_id': self.instructor_id,
            'assigned_courses': [course.to_dict() for course in self.assigned_courses]
        })
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Instructor':
        """
        Create an Instructor object from a dictionary.

        :param data: A dictionary containing instructor data.
        :type data: dict
        :return: An Instructor instance created from the dictionary.
        :rtype: Instructor
        """
        assigned_courses = [Course.from_dict(course) for course in data.get('assigned_courses', [])]
        return Instructor(
            name=data['name'],
            age=data['age'],
            email=data['email'],
            instructor_id=data['instructor_id'],
            assigned_courses=assigned_courses  
        )

class Course:
    """
    A class representing a course with enrolled students and an assigned instructor.
    """
    def __init__(self, course_id: str, course_name: str, instructor: Instructor):
        """
        Initialize a new instance of the Course class.

        :param course_id: The ID of the course.
        :type course_id: str
        :param course_name: The name of the course.
        :type course_name: str
        :param instructor: The instructor assigned to the course.
        :type instructor: Instructor
        """
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []
    
    def add_student(self, student: Student):
        """
        Add a student to the course.

        :param student: The student to add to the course.
        :type student: Student
        """
        self.enrolled_students.append(student)
        print(f"Student '{student.name}' has been added to course '{self.course_name}'.")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the course object to a dictionary.

        :return: A dictionary representation of the course.
        :rtype: dict
        """
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor': self.instructor.to_dict() if self.instructor else None,
            'enrolled_students': [student.to_dict() for student in self.enrolled_students]
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Course':
        """
        Create a Course object from a dictionary.

        :param data: A dictionary containing course data.
        :type data: dict
        :return: A Course instance created from the dictionary.
        :rtype: Course
        """
        course = Course(
            course_id=data['course_id'],
            course_name=data['course_name'],
            instructor=Instructor.from_dict(data['instructor']) if data.get('instructor') else None
        )
        course.enrolled_students = [Student.from_dict(student) for student in data.get('enrolled_students', [])]
        return course



    def save_to_file(self, filename: str):
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file, indent=4)
    
    @staticmethod
    def load_from_file(filename: str) -> 'Course':
        with open(filename, 'r') as file:
            data = json.load(file)
            return Course.from_dict(data)

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class SchoolManagementSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("800x600")

        self.students = []
        self.instructors = []
        self.courses = []

        self.create_gui()
        #self.load_data_from_db()

    def create_gui(self):
        self.tab_control = ttk.Notebook(self.root)
        self.student_tab = ttk.Frame(self.tab_control)
        self.instructor_tab = ttk.Frame(self.tab_control)
        self.course_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.student_tab, text="Students")
        self.tab_control.add(self.instructor_tab, text="Instructors")
        self.tab_control.add(self.course_tab, text="Courses")
        self.tab_control.pack(expand=1, fill='both')
        self.create_student_form(self.student_tab)
        self.create_instructor_form(self.instructor_tab)
        self.create_course_form(self.course_tab)
        self.create_record_display_area()
        self.create_edit_delete_buttons()
        self.create_save_load_buttons()

    def load_data_from_db(self):
        try:
            student_records = data.get_all_students() 
            self.students = [Student.from_dict(student) for student in student_records]
            self.tree.delete(*self.tree.get_children())
            for student in self.students:
                self.tree.insert("", tk.END, values=("Student", f"{student.name}, ID: {student.student_id}"))

            instructor_records = data.get_all_instructors()
            self.instructors = [Instructor.from_dict(instructor) for instructor in instructor_records]
            self.course_instructor_combobox['values'] = [instructor.name for instructor in self.instructors]
            for instructor in self.instructors:
                self.tree.insert("", tk.END, values=("Instructor", f"{instructor.name}, ID: {instructor.instructor_id}"))

            course_records = data.get_all_courses()  
            self.courses = []
            for course_data in course_records:
                instructor = next((i for i in self.instructors if i.instructor_id == course_data["instructor"]["instructor_id"]), None)
                course = Course.from_dict(course_data)
                course.instructor = instructor
                self.courses.append(course)
                self.tree.insert("", tk.END, values=("Course", f"{course.course_name}, ID: {course.course_id}"))
                for student in course.enrolled_students:
                    if student not in self.students:
                        self.students.append(student)
            self.course_register_combobox['values'] = [course.course_name for course in self.courses]

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_student_form(self, tab):
        self.student_name_label = tk.Label(tab, text="Name:")
        self.student_name_label.grid(row=0, column=0)
        self.student_name_entry = tk.Entry(tab)
        self.student_name_entry.grid(row=0, column=1)

        self.student_age_label = tk.Label(tab, text="Age:")
        self.student_age_label.grid(row=1, column=0)
        self.student_age_entry = tk.Entry(tab)
        self.student_age_entry.grid(row=1, column=1)

        self.student_email_label = tk.Label(tab, text="Email:")
        self.student_email_label.grid(row=2, column=0)
        self.student_email_entry = tk.Entry(tab)
        self.student_email_entry.grid(row=2, column=1)

        self.student_id_label = tk.Label(tab, text="Student ID:")
        self.student_id_label.grid(row=3, column=0)
        self.student_id_entry = tk.Entry(tab)
        self.student_id_entry.grid(row=3, column=1)

        self.course_register_label = tk.Label(tab, text="Register for Course:")
        self.course_register_label.grid(row=4, column=0)
        self.course_register_combobox = ttk.Combobox(tab)
        self.course_register_combobox.grid(row=4, column=1)

        self.register_course_button = tk.Button(tab, text="Register Course", command=self.register_student_to_course)
        self.register_course_button.grid(row=5, column=0, columnspan=2)

        self.add_student_button = tk.Button(tab, text="Add Student", command=self.add_student)
        self.add_student_button.grid(row=6, column=0, columnspan=2)

    def create_instructor_form(self, tab):
        self.instructor_name_label = tk.Label(tab, text="Name:")
        self.instructor_name_label.grid(row=0, column=0)
        self.instructor_name_entry = tk.Entry(tab)
        self.instructor_name_entry.grid(row=0, column=1)

        self.instructor_age_label = tk.Label(tab, text="Age:")
        self.instructor_age_label.grid(row=1, column=0)
        self.instructor_age_entry = tk.Entry(tab)
        self.instructor_age_entry.grid(row=1, column=1)

        self.instructor_email_label = tk.Label(tab, text="Email:")
        self.instructor_email_label.grid(row=2, column=0)
        self.instructor_email_entry = tk.Entry(tab)
        self.instructor_email_entry.grid(row=2, column=1)

        self.instructor_id_label = tk.Label(tab, text="Instructor ID:")
        self.instructor_id_label.grid(row=3, column=0)
        self.instructor_id_entry = tk.Entry(tab)
        self.instructor_id_entry.grid(row=3, column=1)

        self.add_instructor_button = tk.Button(tab, text="Add Instructor", command=self.add_instructor)
        self.add_instructor_button.grid(row=4, column=0, columnspan=2)

    def create_course_form(self, tab):
        self.course_id_label = tk.Label(tab, text="Course ID:")
        self.course_id_label.grid(row=0, column=0)
        self.course_id_entry = tk.Entry(tab)
        self.course_id_entry.grid(row=0, column=1)

        self.course_name_label = tk.Label(tab, text="Course Name:")
        self.course_name_label.grid(row=1, column=0)
        self.course_name_entry = tk.Entry(tab)
        self.course_name_entry.grid(row=1, column=1)

        self.course_instructor_label = tk.Label(tab, text="Instructor:")
        self.course_instructor_label.grid(row=2, column=0)
        self.course_instructor_combobox = ttk.Combobox(tab)
        self.course_instructor_combobox.grid(row=2, column=1)

        self.add_course_button = tk.Button(tab, text="Add Course", command=self.add_course)
        self.add_course_button.grid(row=3, column=0, columnspan=2)

    def create_record_display_area(self):
        self.tree = ttk.Treeview(self.root, columns=("Type", "Details"), show="headings")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Details", text="Details")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def create_edit_delete_buttons(self):
        self.edit_delete_frame = tk.Frame(self.root)
        self.edit_delete_frame.pack()
        self.edit_button = tk.Button(self.edit_delete_frame, text="Edit", command=self.edit_record)
        self.edit_button.grid(row=0, column=0, padx=5)

        self.delete_button = tk.Button(self.edit_delete_frame, text="Delete", command=self.delete_record)
        self.delete_button.grid(row=0, column=1, padx=5)

    def create_save_load_buttons(self):
        self.save_load_frame = tk.Frame(self.root)
        self.save_load_frame.pack()
        self.save_button = tk.Button(self.save_load_frame, text="Save Data", command=self.save_data)
        self.save_button.grid(row=0, column=0, padx=5)

        self.load_button = tk.Button(self.save_load_frame, text="Load Data", command=self.load_data)
        self.load_button.grid(row=0, column=1, padx=5)

    def register_student_to_course(self):
        course_name = self.course_register_combobox.get()
        student_name = self.student_name_entry.get()
        
        try:
            data.register_student_to_course(student_name, course_name)  
            messagebox.showinfo("Success", f"Student '{student_name}' registered for course '{course_name}'.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_student(self):
        name = self.student_name_entry.get()
        age = int(self.student_age_entry.get())
        email = self.student_email_entry.get()
        student_id = self.student_id_entry.get()

        try:
            data.add_student(name, age, email, student_id)  
            self.tree.insert("", tk.END, values=("Student", f"{name}, ID: {student_id}"))
            messagebox.showinfo("Success", "Student added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_instructor(self):
        name = self.instructor_name_entry.get()
        age = int(self.instructor_age_entry.get())
        email = self.instructor_email_entry.get()
        instructor_id = self.instructor_id_entry.get()

        try:
            data.add_instructor(name, age, email, instructor_id)  
            self.course_instructor_combobox['values'] = data.get_all_instructors()  
            self.tree.insert("", tk.END, values=("Instructor", f"{name}, ID: {instructor_id}"))
            messagebox.showinfo("Success", "Instructor added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_course(self):
        course_id = self.course_id_entry.get()
        course_name = self.course_name_entry.get()
        instructor_name = self.course_instructor_combobox.get()

        try:
            data.add_course(course_id, course_name, instructor_name)  
            self.course_register_combobox['values'] = data.get_all_courses()  
            self.tree.insert("", tk.END, values=("Course", f"{course_name}, ID: {course_id}"))
            messagebox.showinfo("Success", "Course added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def edit_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No record selected.")
            return
        
        messagebox.showinfo("Info", "Edit feature is not implemented in this example.")

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No record selected.")
            return

        self.tree.delete(selected_item)
        messagebox.showinfo("Info", "Record deleted successfully!")

    def save_data(self):
        data = {
            "students": [student.to_dict() for student in self.students],
            "instructors": [instructor.to_dict() for instructor in self.instructors],
            "courses": [course.to_dict() for course in self.courses]
        }
        with open("school_data.json", "w") as file:
            json.dump(data, file, indent=4)
        messagebox.showinfo("Success", "Data saved successfully!")

    def load_data(self):
        if not os.path.exists("school_data.json"):
            messagebox.showerror("Error", "No saved data file found.")
            return

        with open("school_data.json", "r") as file:
            data = json.load(file)

        self.students.clear()
        self.instructors.clear()
        self.courses.clear()
        self.tree.delete(*self.tree.get_children())
        for student_data in data.get("students", []):
            student = Student.from_dict(student_data)
            self.students.append(student)
            self.tree.insert("", tk.END, values=("Student", f"{student.name}, ID: {student.student_id}"))

        for instructor_data in data.get("instructors", []):
            instructor = Instructor.from_dict(instructor_data)
            self.instructors.append(instructor)
            self.course_instructor_combobox['values'] = [instructor.name for instructor in self.instructors]
            self.tree.insert("", tk.END, values=("Instructor", f"{instructor.name}, ID: {instructor.instructor_id}"))

        for course_data in data.get("courses", []):
            instructor = next((i for i in self.instructors if i.name == course_data["instructor"]["name"]), None)
            course = Course(course_data["course_id"], course_data["course_name"], instructor)
            for student_data in course_data.get("enrolled_students", []):
                student = Student.from_dict(student_data)
                course.enrolled_students.append(student)
            self.courses.append(course)
            self.tree.insert("", tk.END, values=("Course", f"{course.course_name}, ID: {course.course_id}"))

        messagebox.showinfo("Success", "Data loaded successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolManagementSystemApp(root)
    root.mainloop()
