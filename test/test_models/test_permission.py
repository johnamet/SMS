#!/usr/bin/python3
"""
Tests for the permission model.
"""
import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Staff
from models.permission import Permission


class TestPermissionModel(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

        self.head_teacher = Staff(id="1", first_name="John", last_name="Doe", email="john.doe@example.com",
                                  marital_status="Single")

        self.permission = Permission(
            permission_name="view_dashboard",
            role_id="admin",
            assigned_user_id=self.head_teacher.id,
            permission_desc="Allows access to the dashboard"
        )

    def test_permission(self):
        self.assertTrue(self.permission is not None)

    def test_create_permission(self):
        self.session.add_all([self.head_teacher, self.permission])
        self.session.commit()

        queried_permission = self.session.query(Permission).first()
        self.assertTrue(queried_permission is not None)

    def test_permission_name(self):
        self.assertEqual(self.permission.permission_name, "view_dashboard")

    def test_role_id(self):
        self.assertEqual(self.permission.role_id, "admin")

    def test_assigned_user_id(self):
        self.assertEqual(self.permission.assigned_user_id, self.head_teacher.id)

    def test_permission_desc(self):
        self.assertEqual(self.permission.permission_desc, "Allows access to the dashboard")

    def test_created_at(self):
        self.assertTrue(self.permission.created_at < datetime.now())

    def test_updated_at(self):
        self.assertTrue(self.permission.updated_at < datetime.now())

    def test_update(self):
        self.permission.update(permission_desc="Allows read-only access to the dashboard")
        self.assertEqual(self.permission.permission_desc, "Allows read-only access to the dashboard")
        self.assertTrue(self.permission.updated_at > self.permission.created_at)


if __name__ == '__main__':
    unittest.main()
