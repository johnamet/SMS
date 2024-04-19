#!/usr/bin/python3
import unittest
from datetime import datetime

from models.attendance import Attendance


class TestAttendanceModel(unittest.TestCase):
    def setUp(self):
        self.attendance = Attendance(
            class_id="class_1",
            student_id="student_1",
            term="Term 1",
            status=1
        )

    def test_attendance(self):
        self.assertTrue(self.attendance is not None)

    def test_class_id(self):
        self.assertEqual(self.attendance.class_id, "class_1")

    def test_student_id(self):
        self.assertEqual(self.attendance.student_id, "student_1")

    def test_term(self):
        self.assertEqual(self.attendance.term, "Term 1")

    def test_status(self):
        self.assertEqual(self.attendance.status, 1)

    def test_created_at(self):
        self.assertTrue(self.attendance.created_at < datetime.now())

    def test_updated_at(self):
        self.assertTrue(self.attendance.updated_at < datetime.now())

    def test_update(self):
        self.attendance.update(status=0)
        self.assertEqual(self.attendance.status, 0)
        self.assertTrue(self.attendance.updated_at > self.attendance.created_at)


if __name__ == '__main__':
    unittest.main()
