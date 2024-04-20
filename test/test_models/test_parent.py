#!/usr/bin/python3
import unittest
from datetime import datetime

from models.parent import Parent
from models.user import User


class TestParentModel(unittest.TestCase):
    def setUp(self):
        self.user = User("John", "Ametepe",
                         "john@gmail.com", "password")
        self.parent = Parent(
            id=self.user.id,
            marital_status="Married",
            occupation="Engineer"
        )

    def test_parent(self):
        self.assertTrue(self.parent is not None)

    def test_id(self):
        self.assertEqual(self.parent.id, self.user.id)

    def test_marital_status(self):
        self.assertEqual(self.parent.marital_status, "Married")

    def test_occupation(self):
        self.assertEqual(self.parent.occupation, "Engineer")

    def test_created_at(self):
        self.assertTrue(self.parent.created_at < datetime.now())

    def test_updated_at(self):
        self.assertTrue(self.parent.updated_at < datetime.now())

    def test_update(self):
        self.parent.update(occupation="Doctor")
        self.assertEqual(self.parent.occupation, "Doctor")
        self.assertTrue(self.parent.updated_at > self.parent.created_at)


if __name__ == '__main__':
    unittest.main()
