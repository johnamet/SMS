#!/usr/bin/env python3
import unittest
import datetime

from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker

from models import Student, Class
from models.attendance import Attendance
from models.basemodel import Base


class TestAttendanceModel(unittest.TestCase):

    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

        self.student = Student(first_name="John", last_name="Doe", email="johndoe@localhost",
                               password="**HASHED_PASSWORD**",  # Use a secure hashing algorithm
                               other_names="Ametepe", gender="Male",
                               expected_graduation=datetime.datetime(year=2019, month=1, day=1),
                               admission_date=datetime.datetime(year=2019, month=1, day=1),
                               parent_id="1234")
        self.classe = Class(class_name="B7B", head_class_teacher="1245", academic_year="2023/24")

        self.session.add(self.student)
        self.session.add(self.classe)
        self.attendance = Attendance(
            class_id=self.classe.id,
            student_id=self.student.id,
            term="Term 1",
            status=1,
            academic_year="2023/24"
        )

    def test_create_attendance(self):
        self.session.add(self.student)
        self.session.add(self.classe)
        self.session.add(self.attendance)
        self.session.commit()

        self.assertIsNotNone(self.attendance.id)

    def test_query_attendance(self):
        self.session.add(self.student)
        self.session.add(self.classe)
        self.session.add(self.attendance)
        self.session.commit()

        queried_attendance = self.session.query(Attendance).all()

        self.assertIsNotNone(queried_attendance)
        self.assertEqual(len(queried_attendance), 1)

    def test_attendance_student_relationship(self):
        self.session.add(self.student)
        self.session.add(self.classe)
        self.session.add(self.attendance)
        self.session.commit()

        queried_attendance = self.session.query(Attendance).first()
        queried_student = self.session.query(Student).first()
        self.assertIsNotNone(queried_attendance.student)
        self.assertEqual(queried_student, queried_attendance.student)

    def test_student_attendance_relationship(self):
        self.new_attendance = Attendance(
            class_id=self.classe.id,
            student_id=self.student.id,
            term="Term 1",
            status=1,
            academic_year="2023/24"
        )
        self.session.add(self.new_attendance)
        self.session.add(self.student)
        self.session.add(self.classe)
        self.session.add(self.attendance)
        self.session.commit()
        queried_attendance = self.session.query(Attendance).all()
        queried_student = self.session.query(Student).first()
        student_attendances = queried_student.attendances

        self.assertEqual(len(queried_attendance), len(student_attendances))

    def test_class_attendance_relationship(self):
        self.new_attendance = Attendance(
            class_id=self.classe.id,
            student_id=self.student.id,
            term="Term 1",
            status=1,
            academic_year="2023/24"
        )
        self.session.add(self.new_attendance)
        self.session.add(self.student)
        self.session.add(self.classe)
        self.session.add(self.attendance)
        self.session.commit()
        queried_attendance = self.session.query(Attendance).all()
        queried_class = self.session.query(Class).first()
        print(queried_class.attendances)
        self.assertEqual(len(queried_attendance), len(queried_class.attendances))

    def test_attendance_class_relationship(self):
        self.session.add(self.student)
        self.session.add(self.classe)
        self.session.add(self.attendance)
        self.session.commit()

        queried_attendance = self.session.query(Attendance).first()
        queried_class = self.session.query(Class).first()

        self.assertEqual(queried_attendance.classe, queried_class)

    def test_attendance(self):
        self.assertTrue(self.attendance is not None)

    def test_class_id(self):
        self.assertEqual(self.attendance.class_id, self.classe.id)

    def test_student_id(self):
        self.assertEqual(self.attendance.student_id, self.student.id)

    def test_term(self):
        self.assertEqual(self.attendance.term, "Term 1")

    def test_status(self):
        self.assertEqual(self.attendance.status, 1)

    def test_created_at(self):
        self.assertTrue(self.attendance.created_at < datetime.datetime.now())

    def test_updated_at(self):
        self.assertTrue(self.attendance.updated_at < datetime.datetime.now())

    def test_update(self):
        self.attendance.update(status=0)
        self.assertEqual(self.attendance.status, 0)
        self.assertTrue(self.attendance.updated_at > self.attendance.created_at)


if __name__ == '__main__':
    unittest.main()
