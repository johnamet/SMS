#!/usr/bin/python3

"""
Class Management Module

This module provides functionality for managing classes in the school system,
including marking attendance, retrieving class information, enrolling and
unenrolling students, and more.
"""

from models import Class, storage, Student, ClassCourseAssociation, Course
from modules import class_management
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
        self.term = None
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
                                                               term=self.term,
                                                               academic_year=self._class.academic_year)

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

            return self._class.students
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

            return (self._attendance_management.get_attendance(**kwargs)[0],
                    len(self._attendance_management.get_attendance()[0]))
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

    def get_class(self, class_id=None):
        """
        Get a class by id

        Args:
            class_id (str, optional): The ID of the class to query

        Returns:
            Class: The class object.
        """
        if self.class_id is None and class_id:
            self.class_id = class_id

        if self.class_id:
            class_ = storage.get_by_id(Class, self.class_id)
        else:
            raise (Exception("Class id cannot be None"))

        return class_

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
            class_ = None

            if not self.class_id and class_id is not None:
                self.class_id = class_id

            if not self.class_id and class_id is None:
                raise ValueError('class_id cannot be None')

            student = storage.get_by_id(Student, student_id)

            if student is not None:
                class_ = self.get_class(class_id)
                if class_:
                    association = StudentClassAssociation(class_id=class_id, )
                    association.student = student
                    class_.students.append(association)
                else:
                    return False, f"Class with id {class_.id} not found"

                class_.save()
                return True, f"Student {student.first_name} enrolled successfully"
            else:
                return False, f"Student with id {student_id} not found"
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
                return (storage.get_by_id(Student, student_id) is None,
                        "Student unenrolled successfully")
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
            if self._validate_courses_list(courses_list):
                for course in courses_list:
                    association = ClassCourseAssociation()
                    association.course = course
                    class_.courses.append(association)
            else:
                raise ValueError("courses_list contains or is invalid.")
        try:
            storage.save(class_)
            return (storage.get_by_id(Class, class_.id) is not None,
                    "Class successfully created")
        except Exception as e:
            return False, f"Error creating class: {str(e)}"

    def get_classes(self):
        """
        Returns a list of all classes.
        """

        try:
            query = storage.query(Class)
        except Exception as e:
            return None, f"Error getting classes: {str(e)}"

        return query.all(), f"Classes successfully retrieved"

    def update_class(self, class_id, **class_info):
        """
        Update information of an existing class.

        Args:
            class_id (int): The ID of the class to update.
            class_info (dict): A dictionary containing updated class information.

        Returns:
            tuple: A tuple containing the ID of the updated class and a message indicating success or failure.
        """
        try:
            class_ = storage.get_by_id(Class, class_id)
            if not class_:
                raise ValueError("Class does not exist")
            for key, value in class_info.items():
                setattr(class_, key, value)
            storage.save(class_)
            return class_id, "Class updated successfully"
        except Exception as e:
            return None, f"Failed to update class: {str(e)}"

    def delete_class(self, class_id):
        """
        Delete an existing class.

        Args:
            class_id (int): The ID of the class to delete.
        """
        try:
            class_ = storage.get_by_id(Class, class_id)
            if class_:
                # Delete associated records like attendance, gradebooks, etc.
                for attendance_record in class_.attendances:
                    storage.delete(attendance_record)
                for gradebook in class_.gradebooks:
                    storage.delete(gradebook)
                storage.delete(class_)
        except Exception as e:
            return f"Failed to delete class: {str(e)}"

    # def get_class_schedule(self, class_id):
    #     """
    #     Get the schedule of a class.
    #
    #     Args:
    #         class_id (int): The ID of the class.
    #
    #     Returns:
    #         dict: A dictionary containing the schedule details of the class.
    #     """
    #     try:
    #         class_ = storage.get_by_id(Class, class_id)
    #         if not class_:
    #             raise ValueError("Class does not exist")
    #
    #         # Retrieve schedule details from the class object or associated records
    #         # Implement according to how schedule information is stored in your system
    #
    #         return schedule_details, "Class schedule retrieved successfully"
    #     except Exception as e:
    #         return None, f"Failed to retrieve class schedule: {str(e)}"

    def search_classes(self, query):
        """
        Search for classes based on various criteria.

        Args:
            query (str): The search query.

        Returns:
            list: A list of classes matching the search criteria.
        """
        try:
            # Implement the search logic based on criteria like class name, teachers, academic year, etc.
            # Return a list of classes that match the search query
            classes = []  # Implement the search logic here
            return classes, "Classes retrieved successfully"
        except Exception as e:
            return None, f"Failed to search classes: {str(e)}"

    def get_class_details(self, class_id):
        """
        Get comprehensive details about a class.

        Args:
            class_id (str): The ID of the class.

        Returns:
            dict: A dictionary containing comprehensive details of the class.
        """
        try:
            class_ = storage.get_by_id(Class, class_id)
            if not class_:
                raise ValueError("Class does not exist")

            # Serialize the class object to extract details
            # Include information about enrolled students, associated courses, attendance records, gradebooks, etc.
            class_details = class_.serialize()

            class_details["grades"] = [grade.serialize() for grade in class_.gradebooks]
            class_details["attendances"] = [attendance.serialize() for attendance in class_.attendances]
            class_details["students"] = [student.serialize() for student in class_.students]

            return class_details, "Class details retrieved successfully."
        except Exception as e:
            return None, f"Failed to retrieve class details: {str(e)}"

    def get_classes_paginated(self, page=1, page_size=10):
        """
        Get a list of classes with pagination.

        Args:
            page (int): The page number to retrieve (default is 1).
            page_size (int): The number of classes per page (default is 10).

        Returns:
            tuple: A tuple containing a list of classes, total number of classes, and a message indicating success or failure.
        """
        try:
            classes_query = storage.query(Class)
            total_classes = classes_query.count()

            # Calculate offset and limit based on pagination parameters
            offset = (page - 1) * page_size
            limit = page_size

            # Retrieve classes for the current page
            classes = classes_query.offset(offset).limit(limit).all()

            return classes, total_classes, "Classes retrieved successfully"
        except Exception as e:
            return None, 0, f"Failed to retrieve classes: {str(e)}"
