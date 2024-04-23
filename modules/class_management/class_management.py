#!/usr/bin/python3

"""
Class Management Module

This module provides functionality for managing classes in the school system,
including marking attendance, retrieving class information, enrolling and
unenrolling students, and more.
"""

from models import Class, storage, Student, ClassCourseAssociation, Course
from modules.attendance_tracking.attendance_management import AttendanceManagement
from models.class_student_association import StudentClassAssociation


class ClassManagement:
    """
    ClassManagement class provides methods for managing classes in the school system.
    """

    def __init__(self, class_id=None):
        """
        Initializes the ClassManagement instance with optional class_id parameter.

        Args:
            class_id (int, optional): The ID of the class to manage. Defaults to None.
        """
        self.class_id = class_id
        self._class = None
        self._attendance_management = None

    @property
    def _class(self):
        """
        Getter method for the class attribute.

        Returns:
            Class: The class object.
        """
        if self.class_id:
            return self._class

    @_class.setter
    def _class(self, value):
        """
        Setter method for the class attribute.

        Args:
            value (Class): The class object to set.
        """
        if self.class_id:
            self._class = storage.get_by_id(Class, self.class_id)

    @property
    def _attendance_management(self):
        """
        Getter method for the attendance_management attribute.

        Returns:
            AttendanceManagement: The attendance management object.
        """
        return self._attendance_management

    @_attendance_management.setter
    def _attendance_management(self, value):
        """
        Setter method for the attendance_management attribute.

        Args:
            value (AttendanceManagement): The attendance management object to set.
        """
        if self.class_id:
            self._attendance_management = AttendanceManagement(class_id=self._class.id,
                                                               term=self._class.term,
                                                               academic_year=self._class.academic_year)

    def mark_class_attendance(self, present, absent, class_id=None):
        """
        Mark class attendance as present or absent.

        Args:
            present (list): List of student IDs of students present.
            absent (list): List of student IDs of students absent.
            class_id (int, optional): The ID of the class. Defaults to None.

        Returns:
            tuple: A tuple indicating the success status and a message.
        """
        try:
            if not self.class_id and class_id is None:
                raise ValueError('class_id cannot be None')

            if not self.class_id and class_id is not None:
                self.class_id = class_id

            if self._class:
                attendances = []
                for student_id in present:
                    attendance = self._attendance_management.create_attendance(student_id, 1)
                    attendances.append(attendance)

                for student_id in absent:
                    attendance = self._attendance_management.create_attendance(student_id, 0)
                    attendances.append(attendance)

                self._attendance_management.mark_attendance(attendances=attendances)
                return True, "Marked today's class attendance"
            else:
                return False, "Could not find class with class id"
        except Exception as e:
            return False, f"Error marking attendance: {str(e)}"

    def get_students(self, class_id=None):
        """
        Get a list of students in the class.

        Args:
            class_id (int, optional): The ID of the class. Defaults to None.

        Returns:
            list: A list of Student objects.
        """
        try:
            if not self.class_id and class_id is None:
                raise ValueError('class_id cannot be None')

            if not self.class_id and class_id is not None:
                self.class_id = class_id
                self.__init__(self.class_id)

            students_id = self._class.students
            return [storage.get_by_id(Student, student_id) for student_id in students_id]
        except Exception as e:
            return [], f"Error getting students: {str(e)}"

    def get_class_attendance(self, class_id=None, **kwargs):
        """
        Get class attendance.

        Args:
            class_id (int, optional): The ID of the class. Defaults to None.
            **kwargs: Additional keyword arguments for filtering.

        Returns:
            tuple: A tuple containing attendance records and the count of records.
        """
        try:
            if not self.class_id and class_id is not None:
                self.class_id = class_id
                self.__init__(self.class_id)

            if not self.class_id and class_id is None:
                raise ValueError('class_id cannot be None')

            return (self._attendance_management.get_attendance(**kwargs),
                    len(self._attendance_management.get_attendance()))
        except Exception as e:
            return [], f"Error getting class attendance: {str(e)}"

        # Add input validation to methods

    def _validate_student(self, student_id):
        """
        Validate the student by querying the database to find the student.

        Args:
            student_id (str): The ID of the student.

        Returns:
            bool: True if the student ID is valid, False otherwise.
        """
        student = storage.get_by_id(Student, student_id)
        return student is not None and isinstance(student, Student)

    def _validate_courses_list(self, courses_list):
        """
        Validate the courses list.

        Args:
            courses_list (list): List of course objects.

        Returns:
            bool: True if the courses list is valid, False otherwise.
        """
        return isinstance(courses_list, list) and all(isinstance(course, Course) for course in courses_list)

    # Implement methods for enrollment, unenrollment, and class creation

    def enroll_student(self, class_id=None, student_id=None):
        """
        Enroll a student in the class.

        Args:
            class_id (int, optional): The ID of the class. Defaults to None.
            student_id (int): The ID of the student to enroll.

        Returns:
            tuple: A tuple indicating the success status and a message.
        """
        try:
            if not self.class_id and class_id is not None:
                self.class_id = class_id
                self.__init__(self.class_id)

            if not self.class_id and class_id is None:
                raise ValueError('class_id cannot be None')

            student = storage.get_by_id(Student, student_id)

            if student:
                association = StudentClassAssociation()
                association.student = student
                self._class.students.append(association)
                storage.save()
                return True, "Student enrolled successfully"
            else:
                return False, "Student not found"
        except Exception as e:
            return False, f"Error enrolling student: {str(e)}"

    def unenroll_student(self, class_id=None, student_id=None):
        """
        Unenroll a student from the class.

        Args:
            class_id (int, optional): The ID of the class. Defaults to None.
            student_id (int): The ID of the student to unenroll.

        Returns:
            tuple: A tuple indicating the success status and a message.
        """
        try:
            if not self.class_id and class_id is not None:
                self.class_id = class_id
                self.__init__(self.class_id)

            if not self.class_id and class_id is None:
                raise ValueError('class_id cannot be None')

            student = storage.get_by_id(Student, student_id)
            if student:
                association = StudentClassAssociation()
                association.student = student
                self._class.students.remove(association)
                storage.save()
                return True, "Student unenrolled successfully"
            else:
                return False, "Student not found"
        except Exception as e:
            return False, f"Error unenrolling student: {str(e)}"

    def create_class(self, class_name,
                     head_class_teacher,
                     academic_year,
                     courses_list,
                     assist_class_teacher=None,
                     students_list=None,
                     id=None, ):
        """
        Creates a new class
        Args:
            class_name (str): The name of the class.
            head_class_teacher (str): The ID of the teacher of the class.
            academic_year (str): The academic year of the class.
            courses_list (list): A list of courses that the class belongs to.
            assist_class_teacher (str): The ID of the teacher of the class.
            students_list (list): A list of students that the class belongs to.
            id (str): The ID of the class.
        """
        if students_list is None:
            students_list = []

        if not self._validate_courses_list(courses_list):
            raise ValueError("courses_list cannot be None,"
                             "add at least one course")

        class_ = Class(class_name=class_name,
                       head_class_teacher=head_class_teacher,
                       academic_year=academic_year,
                       assist_class_teacher=assist_class_teacher,
                       id=id)

        if students_list:
            for student in students_list:
                if self._validate_student(student):
                    st = storage.get_by_id(Student, student)
                    association = StudentClassAssociation()
                    association.student = st
                    class_.students.append(association)

        if courses_list:
            for course in courses_list:
                association = ClassCourseAssociation()
                association.course = course
                class_.courses.append(association)
        try:
            storage.save(class_)
            return True, "Class successfully created"
        except Exception as e:
            return False, f"Error creating class: {str(e)}"
