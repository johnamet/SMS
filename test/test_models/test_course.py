import unittest
from models.course import Course
from datetime import datetime


class TestCourseModel(unittest.TestCase):
    def setUp(self):
        self.course = Course(
            course_name="Mathematics",
            course_description="Introduction to Algebra",
            teacher_id="12345"
        )

    def test_course(self):
        self.assertTrue(self.course is not None)

    def test_course_name(self):
        self.assertEqual(self.course.course_name, "Mathematics")

    def test_course_description(self):
        self.assertEqual(self.course.course_description, "Introduction to Algebra")

    def test_teacher_id(self):
        self.assertEqual(self.course.teacher_id, "12345")

    def test_created_at(self):
        self.assertTrue(self.course.created_at < datetime.now())

    def test_updated_at(self):
        self.assertTrue(self.course.updated_at < datetime.now())

    def test_update(self):
        self.course.update(course_description="Advanced Algebra")
        self.assertEqual(self.course.course_description, "Advanced Algebra")
        self.assertTrue(self.course.updated_at > self.course.created_at)


if __name__ == '__main__':
    unittest.main()
