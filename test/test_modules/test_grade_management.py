#!/usr/bin/python3

import unittest
from datetime import datetime

from models import Grade, storage, Course, Class, Student  # Assuming models.py defines Grade and storage
from modules.gradebook_management.gradebook_management import GradebookManagement
from modules.test_utils import create_staff_member


class TestGradebookManagement(unittest.TestCase):

    def setUp(self):
        """
        Create sample gradebook data for testing.
        """
        self.teacher, self.parent = create_staff_member()
        self.course = Course(course_name="Mathematics", course_description="Introduction to Algebra",
                             teacher_id=self.teacher.id)
        self.course.save()

        self.class_ = Class(class_name="B7B", head_class_teacher=self.teacher.id, academic_year="2023/24")
        self.class_.save()

        self.student = Student(first_name="John",
                               last_name="Doe",
                               email="johndoe@example.com",
                               password="password!P123", parent_id=self.parent.id,
                               admission_date=datetime.today(),
                               gender="Male",
                               expected_graduation=datetime(2025, 1, 5))
        self.student.save()
        self.grade1 = Grade(grade=85, grade_desc="Homework", term="Term 1", course_id=self.course.id,
                            class_id=self.class_.id,
                            out_of=100,
                            student_id=self.student.id,
                            academic_year="2023/24")
        self.grade1.save()
        self.grade2 = Grade(grade=85, grade_desc="Exam", term="Term 1",
                            course_id=self.course.id,
                            out_of=100,
                            class_id=self.class_.id,
                            student_id=self.student.id,
                            academic_year="2023/24")
        self.grade2.save()
        self.grade3 = Grade(grade=89, grade_desc="Quiz", term="Term 1",
                            out_of=100,
                            course_id=self.course.id,
                            class_id=self.class_.id,
                            student_id=self.student.id,
                            academic_year="2023/24")
        self.grade3.save()

    def tearDown(self):
        """
        Clean up test data after all tests are run.
        """
        storage.delete_by_id(Grade, self.grade1.id)
        storage.delete_by_id(Grade, self.grade2.id)
        storage.delete_by_id(Grade, self.grade3.id)

    def test_get_gradebooks_by_student(self):
        """
        Test retrieving gradebooks for a student.
        """
        gradebook_mgmt = GradebookManagement(student_id=self.student.id)
        grades, message = gradebook_mgmt.get_gradebooks()
        self.assertEqual(len(grades), 3)  # Expect 2 grades for student1
        self.assertEqual(message, "Retrieved gradebook successfully.")

    def test_get_gradebooks_by_class(self):
        """
        Test retrieving gradebooks for a class.
        """
        gradebook_mgmt = GradebookManagement(class_id=self.class_.id)
        grades, message = gradebook_mgmt.get_gradebooks()
        self.assertEqual(len(grades), 3)  # Expect 3 grades for class1
        self.assertEqual(message, "Retrieved gradebook successfully.")

    def test_get_gradebook_by_id(self):
        """
        Test retrieving a gradebook by its ID.
        """
        grade1 = Grade(grade=85, grade_desc="Homework", term="Term 1", course_id=self.course.id,
                       class_id=self.class_.id,
                       out_of=100,
                       student_id=self.student.id,
                       academic_year="2023/24")
        grade1.save()
        gradebook_mgmt = GradebookManagement()
        grade, message = gradebook_mgmt.get_gradebook_by_id(grade1.id)
        self.assertIsNotNone(grade)
        # self.assertEqual(grade.student_id, self.grade1.student_id)
        self.assertEqual(message, "Retrieved gradebook successfully.")

    def test_record_a_grade(self):
        """
        Test creating a new grade.
        """
        new_grade_data = {"student_id": self.student.id, "grade_desc": "Homework",
                          "term": "Term 1", "course_id": self.course.id, "class_id": self.class_.id,
                          "academic_year": "2023/24", "grade": 100, "out_of": 100}

        gradebook_mgmt = GradebookManagement()
        grade, message = gradebook_mgmt.record_a_grade(new_grade_data)
        self.assertIsNotNone(grade)  # Check if a grade object is created
        self.assertEqual(message, "Saved grade successfully.")

    def test_update_grade(self):
        """
        Test updating information of a gradebook.
        """
        gradebook_mgmt = GradebookManagement()
        updated_data = {"grade": 95}
        success, message = gradebook_mgmt.update_grade(self.grade2.id, **updated_data)
        self.assertTrue(success)
        self.assertEqual(message, "Successfully updated gradebook.")

        # Verify update by retrieving again
        updated_grade, msg = gradebook_mgmt.get_gradebook_by_id(self.grade2.id)
        self.assertEqual(updated_grade.grade, 95)

    def test_delete_grade(self):
        """
        Test deleting a gradebook.
        """
        gradebook_mgmt = GradebookManagement()
        success, message = gradebook_mgmt.delete_grade(self.grade3.id)
        self.assertTrue(success)
        self.assertEqual(message, "Gradebook deleted successfully.")

        # Verify deletion by attempting to retrieve
        _, message = gradebook_mgmt.get_gradebook_by_id(self.grade3.id)
        self.assertIn("failed to retrieve", message.lower())

    # def test_get_gradebooks_empty(self):
    #     """
    #     Test retrieving gradebooks when there are none.
    #     """
    #     gradebook_mgmt = GradebookManagement()
    #     # Clear all existing data (assuming you have a way to do this)
    #     storage.delete_all(Grade)
    #
    #     grades, message = gradebook_mgmt.get_gradebooks()
    #     self.assertEqual(len(grades), 0)
    #     self.assertEqual(message, "Retrieved gradebook successfully.")

    def test_record_a_grade_invalid_data(self):
        """
        Test creating a new grade with invalid data.
        """
        gradebook_mgmt = GradebookManagement()
        invalid_data = {"invalid_field": "invalid_value"}
        grade, message = gradebook_mgmt.record_a_grade(invalid_data)
        self.assertIsNone(grade)
        self.assertIn("failed to create gradebook", message.lower())

    def test_update_grade_nonexistent_id(self):
        """
        Test updating a gradebook with a non-existent ID.
        """
        gradebook_mgmt = GradebookManagement()
        success, message = gradebook_mgmt.update_grade(1000, **{"grade": 40})
        self.assertFalse(success)
        self.assertIn("gradebook not found", message.lower())

    def test_delete_grade_nonexistent_id(self):
        """
        Test deleting a gradebook with a non-existent ID.
        """
        gradebook_mgmt = GradebookManagement()
        success, message = gradebook_mgmt.delete_grade(1000)
        self.assertFalse(success)
        self.assertIn("gradebook not found", message.lower())

    if __name__ == "__main__":
        unittest.main()
