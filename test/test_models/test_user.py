import unittest
from datetime import datetime

from models.user import User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.user = User("first", "last",
                         "test@test.com", "password",)
        self.user.contact_number = []
        self.user.feedbacks = []

    def test_user(self):
        self.assertTrue(self.user is not None)

    def test_id(self):
        self.assertTrue(self.user.id is not None)

    def test_first_name(self):
        self.assertTrue(self.user.first_name == "first")

    def test_created_date(self):
        self.assertTrue(self.user.created_at < datetime.now())

    def test_updated_date(self):
        self.assertTrue(self.user.updated_at < datetime.now())

    def test_update(self):
        self.user.update(**{"first_name": "Johnny"})
        self.assertTrue(self.user.first_name == "Johnny")
        self.assertTrue(self.user.updated_at != self.user.created_at)

    def test_last_name(self):
        self.assertEqual(self.user.last_name, "last")

    def test_email(self):
        self.assertEqual(self.user.email, "test@test.com")

    def test_password(self):
        self.assertEqual(self.user.password, "password")

    def test_other_names(self):
        self.assertIsNone(self.user.other_names)

    def test_contact_number(self):
        self.assertListEqual(self.user.contact_number, [])

    def test_address(self):
        self.assertIsNone(self.user.address)

    def test_dob(self):
        self.assertIsNone(self.user.dob)

    def test_last_login_date(self):
        self.assertTrue(self.user.last_login_date < datetime.now())

    def test_registration_date(self):
        self.assertIsNone(self.user.registration_date)


if __name__ == '__main__':
    unittest.main()
