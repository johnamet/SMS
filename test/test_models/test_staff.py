#!/usr/bin/python3
import unittest
from datetime import datetime
from models.staff import Staff
from models.user import User


class TestStaffModel(unittest.TestCase):
    def setUp(self):
        self.user = User(first_name="Johnny", last_name="Ametepe",
                         email='<EMAIL>', password='<PASSWORD>')
        self.staff = Staff(
            staff_id=self.user.id,
            marital_status="Single",
            qualifications=["BSc", "MSc"],
            bank_acc="1234567890",
            department="IT",
            pension_fund_acc="0987654321",
            status="active"
        )

    def test_staff(self):
        self.assertTrue(self.staff is not None)

    def test_staff_id(self):
        self.assertEqual(self.staff.id, self.user.id)

    def test_marital_status(self):
        self.assertEqual(self.staff.marital_status, "Single")

    def test_qualifications(self):
        self.assertListEqual(self.staff.qualifications, ["BSc", "MSc"])

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
