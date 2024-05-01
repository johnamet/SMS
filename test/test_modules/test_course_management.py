#!/usr/bin/python3
import unittest

from models import storage, Course
from modules.course_management.course_management import CourseManagement
from modules.test_utils import *


class TestCourseManagement(unittest.TestCase):
    def setUp(self):
        # Initialize CourseManagement instance
        self.course_management = CourseManagement()
        self.staff, self.parent = create_staff_member()
        self.clss = create_class()
        course_dict = {
            "course_name": "Test Course",
            "course_description": "This is a test course",
            "teacher_id": self.staff.id,
            "class_id": self.clss.id,
        }

        self.course = Course(**course_dict)
        self.course.save()
        self.students = create_students(parent_id=self.parent.id)

    def test_create_course(self):
        # Test creating a new course
        course_dict = {
            "course_name": "Test Course",
            "course_description": "This is a test course",
            "teacher_id": self.staff.id,
            "class_id": self.clss.id,
        }
        course, message = self.course_management.create_course(course_dict)
        self.course = course
        self.assertIsNotNone(course)
        self.assertEqual(message, "Course created successfully")

    def test_get_courses_by_teacher(self):
        # Test getting courses by teacher ID
        teacher_id = self.staff.id  # Replace with a valid teacher ID
        courses, message = self.course_management.get_courses_by_teacher(teacher_id)
        self.assertIsNotNone(courses)
        self.assertEqual(message, "Courses retrieved successfully")

    def test_get_courses_by_class(self):
        # Test getting courses by class ID
        class_id = self.clss.id
        courses, message = self.course_management.get_courses_by_class(class_id)
        self.assertIsNotNone(courses)
        self.assertEqual(message, "Courses retrieved successfully")

    def test_associate_course_with_class(self):
        result, msg = self.course_management.associate_course_with_class(self.course.id, self.clss.id)
        self.assertTrue(result)

    def test_update_course(self):

        update_dict = {"course_name": "Course Test"}

        result, msg = self.course_management.update_course(self.course.id, **update_dict)
        self.assertIsNotNone(result)

    def test_disassociate_course_with_class(self):
        new_class = create_class()
        course_dict = {
            "course_name": "Test Course",
            "course_description": "This is a test course",
            "teacher_id": self.staff.id,
            "class_id": new_class.id
        }
        course, msg = self.course_management.create_course(course_dict)
        result, msg = self.course_management.disassociate_course_from_class(course.id, new_class.id)
        self.assertTrue(result)

    def test_get_course_details(self):
        course, message = self.course_management.get_course_details(self.course.id)
        self.assertIsNotNone(course)
        self.assertIsInstance(course, dict)

    def test_delete_course(self):
        result, msg = self.course_management.delete_course(self.course.id)

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
