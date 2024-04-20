#!/usr/bin/python3
import unittest
import os

from models import BaseModel
from models.engine.filestorage import FileStorage
from models.user import User


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage()
        self.base = BaseModel()
        self.storage.new(self.base)
        self.storage.save()

    def test_file_storage_creation(self):
        self.assertTrue(os.path.exists(self.storage._FileStorage__file_storage_path))

    def test_save_and_reload(self):
        # Create a user object
        user = User(first_name="John", last_name="Doe",
                    email="john@example.com", password="password")
        # Add user to storage
        self.storage.new(user)
        # Save storage to file
        self.storage.save()

        # Create new storage instance
        new_storage = FileStorage()
        # Reload storage from file
        new_storage.reload()

        # Check if the reloaded storage contains the user object
        self.assertIn("User." + user.id, new_storage.all())

    def test_file_save(self):
        # check length for first time save
        self.assertEqual(len(self.storage.all()), 1)

        user = User(first_name="Jane", last_name="Doe",
                    email="john@example.com",
                    password="password")
        self.storage.new(user)
        self.storage.save()

        self.storage.close()

        self.storage.reload()

        self.assertEqual(len(self.storage.all()), 2)

        user.update(**{"password": "PASSWORD"})
        self.storage.new(user)
        self.storage.save()

        self.storage.close()
        self.storage.reload()

        self.assertEqual(len(self.storage.all()), 2)

    def tearDown(self):
        os.remove(self.storage._FileStorage__storage)


if __name__ == '__main__':
    unittest.main()
