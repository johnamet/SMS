#!/usr/bin/python3
import unittest
from datetime import datetime
from models.student import Student


class TestStudentModel(unittest.TestCase):
    def setUp(self):
        self.student = Student(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password",
            parent_id="parent_1",
            expected_graduation=datetime(2026, 6, 30),
            admission_date=datetime(2021, 9, 1)
        )

    def test_student(self):
        self.assertTrue(self.student is not None)

    def test_first_name(self):
        self.assertEqual(self.student.first_name, "John")

    def test_last_name(self):
        self.assertEqual(self.student.last_name, "Doe")

    def test_email(self):
        self.assertEqual(self.student.email, "john@example.com")

    def test_password(self):
        self.assertEqual(self.student.password, "password")

    def test_parent_id(self):
        self.assertEqual(self.student.parent_id, "parent_1")

    def test_expected_graduation(self):
        self.assertEqual(self.student.expected_graduation, datetime(2026, 6, 30))

    def test_admission_date(self):
        self.assertEqual(self.student.admission_date, datetime(2021, 9, 1))

    def test_created_at(self):
        self.assertTrue(self.student.created_at < datetime.now())

    def test_updated_at(self):
        self.assertTrue(self.student.updated_at < datetime.now())

    def test_update(self):
        self.student.update(expected_graduation=datetime(2027, 6, 30))
        self.assertEqual(self.student.expected_graduation, datetime(2027, 6, 30))
        self.assertTrue(self.student.updated_at > self.student.created_at)


if __name__ == '__main__':
    unittest.main()
