#!/usr/bin/python3
import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Course
from models.qualification import Qualification
from models.staff import Staff
from models.user import User


class TestStaffModel(unittest.TestCase):
    def setUp(self):
        # Set up an in-memory SQLite database for testing
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

        self.user = User(first_name="Johnny", last_name="Ametepe",
                         gender="Male",
                         email='<EMAIL>', password='<PASSWORD>')

        self.staff = Staff(
            id=self.user.id,
            marital_status="Single",
            qualifications=["BSc", "MSc"],
            bank_acc="1234567890",
            department="IT",
            pension_fund_acc="0987654321",
            status="active"
        )

        self.course1 = Course(course_name="Mathematics", course_description="B8 mathematics", teacher_id=self.staff.id)
        self.course2 = Course(course_name="Physics", course_description="B7 physics", teacher_id=self.staff.id)
        self.qualification1 = Qualification("Bsc", desc="Mathematics", staff_id=self.staff.id, )
        self.qualification2 = Qualification("Msc", desc="Physics", staff_id=self.staff.id, )

        # Associate courses with staff
        self.staff.courses.append(self.course1)
        self.staff.courses.append(self.course2)
        self.staff.qualifications.append(self.qualification1)
        self.staff.qualifications.append(self.qualification2)

        self.session.add_all([self.staff, self.user, self.course1, self.course2,
                              self.qualification1, self.qualification2])
        self.session.commit()

    def test_staff(self):
        self.session.add_all([self.user, self.staff])
        self.session.commit()
        queried_staff = self.session.query(Staff).all()
        self.assertEqual(queried_staff, [self.staff])

    def test_qualifications_relationship(self):
        queried_staff = self.session.query(Staff).first()
        self.assertEqual(len(queried_staff.qualifications), 2)

    def test_courses_relationship(self):
        queried_staff = self.session.query(Staff).first()
        self.assertEqual(len(queried_staff.courses), 2)
        self.assertIn(self.course1, queried_staff.courses)
        self.assertIn(self.course2, queried_staff.courses)

    def test_staff_id(self):
        self.assertEqual(self.staff.id, self.user.id)

    def test_marital_status(self):
        self.assertEqual(self.staff.marital_status, "Single")

    def test_qualifications(self):
        self.assertListEqual(self.staff.qualification, ["BSc", "MSc"])

    def test_bank_acc(self):
        self.assertEqual(self.staff.bank_acc, "1234567890")

    def test_department(self):
        self.assertEqual(self.staff.department, "IT")

    def test_pension_fund_acc(self):
        self.assertEqual(self.staff.pension_fund_acc, "0987654321")

    def test_status(self):
        self.assertEqual(self.staff.status, "active")

    def test_created_at(self):
        self.assertTrue(self.staff.created_at < datetime.now())

    def test_updated_at(self):
        self.assertTrue(self.staff.updated_at < datetime.now())

    def test_update(self):
        self.staff.update(status="inactive")
        self.assertEqual(self.staff.status, "inactive")
        self.assertTrue(self.staff.updated_at > self.staff.created_at)


if __name__ == '__main__':
    unittest.main()
