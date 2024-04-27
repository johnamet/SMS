#!/usr/bin/python3
"""
Course Management Module
"""
from models import storage, Course, ClassCourseAssociation, Class, User, Staff


class CourseManagement:
    """
    Course Management Module

    This module provides methods to manage courses offered in the school system.
    """

    def __init__(self, teacher_id=None, course_id=None, class_id=None):
        """
        Initialize the CourseManagement instance.

        Args:
            teacher_id (str): The ID of the teacher associated with the course.
            course_id (str): The ID of the course.
            class_id (str): The ID of the class associated with the course.
        """
        self.teacher_id = teacher_id
        self.course_id = course_id
        self.class_id = class_id

    def get_courses(self):
        """
        Get all courses offered in the school system.

        Returns:
            tuple: A tuple containing the courses offered in the school system and a status message.
        """

        try:
            courses = storage.query(Course)
        except Exception as e:
            return None, f"Failed to retrieve courses: {str(e)}"

        return courses, "Retrieved all Courses"

    def create_course(self, course_dict):
        """
        Create a new course.

        Args:
            course_dict (dict): A dictionary containing course information.
                Required keys: 'course_name', 'course_description', 'teacher_id'.

        Returns:
            tuple: A tuple containing the created course object and a message indicating success or failure.
        """
        try:
            if 'teacher_id' not in course_dict:
                raise KeyError("Teacher id cannot be empty")
            if 'course_name' not in course_dict:
                raise KeyError("Course name cannot be empty")
            if 'course_description' not in course_dict:
                raise KeyError("Course description cannot be empty")

            course = Course(**course_dict)
            storage.save(course)

            if "class_id" in course_dict:
                self.associate_course_with_class(course.id, course_dict["class_id"])

            return course, "Course created successfully"
        except Exception as e:
            return None, f"Failed to create course: {str(e)}"

    def get_courses_by_teacher(self, teacher_id):
        """
        Get courses associated with a specific teacher.

        Args:
            teacher_id (str): The ID of the teacher.

        Returns:
            tuple: A tuple containing a list of courses and a message indicating success or failure.
        """

        # Verify if teacher exists
        teacher = storage.get_by_id(Staff, teacher_id)

        if teacher is None:
            raise ValueError("Teacher does not exist")
        try:
            courses = storage.query(Course).filter(Course.teacher_id == teacher_id).all()
            return courses, "Courses retrieved successfully"
        except Exception as e:
            return None, f"Failed to retrieve courses: {str(e)}"

    def get_courses_by_class(self, class_id):
        """
        Get courses associated with a specific class.

        Args:
            class_id (str): The ID of the class.

        Returns:
            tuple: A tuple containing a list of courses and a message indicating success or failure.
        """
        # Check if class exists
        class_ = storage.get_by_id(Class, class_id)

        if class_ is None:
            raise ValueError("Class does not exist")
        try:
            courses = storage.query(Course).join(ClassCourseAssociation).filter(
                ClassCourseAssociation.class_id == class_id).all()
            return courses, "Courses retrieved successfully"
        except Exception as e:
            return None, f"Failed to retrieve courses: {str(e)}"

    def associate_course_with_class(self, course_id, class_id):
        """
        Associate a course with a class.

        Args:
            course_id (str): The ID of the course.
            class_id (str): The ID of the class.

        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        try:
            association = ClassCourseAssociation(course_id=course_id, class_id=class_id)
            storage.save(association)
            return True, "Course associated with class successfully"
        except Exception as e:
            return False, f"Failed to associate course with class: {str(e)}"

    def disassociate_course_from_class(self, course_id, class_id):
        """
        Disassociate a course from a class.

        Args:
            course_id (str): The ID of the course.
            class_id (str): The ID of the class.

        Returns:
            tuple: A tuple containing a boolean indicating success and a message.
        """
        try:
            association = storage.query(ClassCourseAssociation).filter_by(course_id=course_id,
                                                                          class_id=class_id).first()
            if association:
                storage.delete(association)
                return True, "Course disassociated from class successfully"
            else:
                return False, "Course is not associated with the specified class"
        except Exception as e:
            return False, f"Failed to disassociate course from class: {str(e)}"

    def update_course(self, course_id, **course_dict):
        """
        Update an existing course.

        Args:
            course_id (str): The ID of the course to update.
            course_dict (dict): A dictionary containing updated course information.

        Returns:
            tuple: A tuple containing the ID of the updated course and a message indicating success or failure.
        """
        try:
            course = storage.get_by_id(Course, course_id)
            if not course:
                raise ValueError("Course does not exist")
            for key, value in course_dict.items():
                setattr(course, key, value)
            storage.save(course)
            return course_id, "Course updated successfully"
        except Exception as e:
            return None, f"Failed to update course: {str(e)}"

    def delete_course(self, course_id):
        """
        Delete an existing course.

        Args:
            course_id (str): The ID of the course to delete.

        R
        """
        try:
            course = storage.get_by_id(Course, course_id)
            if course:
                storage.delete(course)
            return storage.get_by_id(Course, course_id) is None, "Course deleted successfully"
        except Exception as e:
            print(f"Failed to delete course: {str(e)}")

    def get_grades_by_course(self, course_id):
        """
        Get grades associated with a specific course.

        Args:
            course_id (str): The ID of the course.

        Returns:
            tuple: A tuple containing a list of grades and a message indicating success or failure.
        """
        try:
            if not course_id:
                raise ValueError("Course ID cannot be None")

            course = storage.get_by_id(Course, course_id)
            if not course:
                raise ValueError(f"Course with ID {course_id} not found")

            grades = course.gradebooks
            return grades, "Grades retrieved successfully"
        except ValueError as ve:
            return None, str(ve)
        except Exception as e:
            return None, f"Failed to retrieve grades: {str(e)}"

    def get_courses_paginated(self, page=1, page_size=10):
        """
        Get a list of courses with pagination.

        Args:
            page (int): The page number to retrieve (default is 1).
            page_size (int): The number of courses per page (default is 10).

        Returns:
            tuple: A tuple containing a list of courses, total number of courses, and a message indicating success or failure.
        """
        try:
            courses_query = storage.query(Course)
            total_courses = courses_query.count()

            # Calculate offset and limit based on pagination parameters
            offset = (page - 1) * page_size
            limit = page_size

            # Retrieve courses for the current page
            courses = courses_query.offset(offset).limit(limit).all()

            return courses, total_courses, "Courses retrieved successfully"
        except Exception as e:
            return None, 0, f"Failed to retrieve courses: {str(e)}"

    def get_course_details(self, course_id):
        """
        Get a comprehensive detail about a course

        Args:
            course_id (str): The ID of the course

        Returns:
            tuple: tuple of a dictionary containing a comprehensive detail of the course and success/failure msg
        """
        try:
            if not course_id:
                raise ValueError("Course id cannot be None")

            course = storage.get_by_id(Course, course_id)

            if not course:
                return None, f"Course with id {course_id} was not found"

            # Serialize the course object to extract details
            teacher = storage.get_by_id(User, course.teacher_id)
            course_details = {
                "id": course.id,
                "course_name": course.course_name,
                "course_description": course.course_description,
                "teacher": teacher.first_name + " " + teacher.last_name,
                "classes": [storage.get_by_id(Class, class_assoc.class_id).serialize()
                            for class_assoc in course.classes],
                "gradebooks": [gradebook.serialize() for gradebook in course.gradebooks]
            }

            return course_details, "Retrieved course details successfully."
        except Exception as e:
            return None, f"Failed to retrieve course details: {str(e)}"
