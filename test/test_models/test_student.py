#!/usr/bin/python3
import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Parent, Gradebook, Attendance
from models.student import Student


class TestStudentRelationships(unittest.TestCase):
    def setUp(self):
        # Set up an in-memory SQLite database for testing
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

        # Create sample data for testing relationships
        self.parent = Parent(parent_id="parent_1")
        self.student = Student(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password",
            gender="Male",
            parent_id="parent_1",
            expected_graduation=datetime(2026, 6, 30),
            admission_date=datetime(2021, 9, 1)
        )

        self.parent.students.append(self.student)

        self.gradebook1 = Gradebook(course_id="course_1", student_id=self.student.id, grade=15, class_id="class_id")
        self.gradebook2 = Gradebook(course_id="course_2", student_id=self.student.id, grade=15, class_id="class_id")
        self.attendance1 = Attendance(date=datetime(2024, 4, 20), student_id=self.student.id,
                                      class_id="class_id", term="Term 2", status=1)
        self.attendance2 = Attendance(date=datetime(2024, 4, 21), student_id=self.student.id,
                                      class_id="class_id", term="Term 2", status=1)

        self.session.add_all([self.parent, self.student, self.gradebook1, self.gradebook2,
                              self.attendance1, self.attendance2])
        self.session.commit()

    def test_student_parent_relationship(self):
        queried_student = self.session.query(Student).filter_by(id=self.student.id).first()
        self.assertEqual(queried_student.parent_id, self.parent.id)
        self.assertEqual(queried_student.parents[0], self.parent)

    def test_student_gradebooks_relationship(self):
        queried_student = self.session.query(Student).filter_by(id=self.student.id).first()
        self.assertEqual(len(queried_student.gradebooks), 2)
        self.assertIn(self.gradebook1, queried_student.gradebooks)
        self.assertIn(self.gradebook2, queried_student.gradebooks)

    def test_student_attendances_relationship(self):
        queried_student = self.session.query(Student).filter_by(id=self.student.id).first()
        self.assertEqual(len(queried_student.attendances), 2)
        self.assertIn(self.attendance1, queried_student.attendances)
        self.assertIn(self.attendance2, queried_student.attendances)

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
        self.assertEqual(self.student.expected_graduation, datetime(2026, 6, 30).date())

    def test_admission_date(self):
        self.assertEqual(self.student.admission_date, datetime(2021, 9, 1).date())

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
