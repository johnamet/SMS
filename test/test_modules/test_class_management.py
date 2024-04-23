#!/usr/bin/python3
"""
Tests for class management
"""
import unittest
from models import Class
from modules.class_management.class_management import ClassManagement


class ClassManagementTestCase(unittest.TestCase):
    def setUp(self):
        self.class_management = ClassManagement()


if __name__ == '__main__':
    unittest.main()
