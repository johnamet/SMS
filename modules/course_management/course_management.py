#!/usr/bin/python3
"""
Course Management Module
"""
from models import storage, Course


class CourseManagement:
    """
    Course Management Module
    """

    def __init__(self, academic_year=None, course_id=None, class_id=None):
        self.academic_year = academic_year
        self.course_id = course_id
        self.clas_id = class_id

    def create_course(self, course_name, course_description, course_teacher):
        """
        Create a new course
        """
        course = Course(course_name, course_description, course_teacher)
        storage.new(course)

    def delete_course(self, course_id):
        course = storage.get_by_id(course_id)
        storage.delete(course)