#!/usr/bin/python3
import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Student, Base
from models.parent import Parent
from models.user import User


class TestParentModel(unittest.TestCase):
    def setUp(self):
        # Set up an in-memory SQLite database for testing
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

        self.user = User("John", "Ametepe",
                         "john@gmail.com", "password",gender="Male")
        self.parent = Parent(
            parent_id=self.user.id,
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

    def test_missing_fields(self):
        with self.assertRaises(TypeError):
            parent = Parent()  # Missing required field parent_id
            self.session.add(parent)
            self.session.commit()

    def test_relationship(self):
        # Add a child to the parent and test if it's correctly associated
        child = Student(first_name="John", last_name="Doe", email="johndoe@localhost",
                        password="**HASHED_PASSWORD**",  # Use a secure hashing algorithm
                        other_names="Ametepe", gender="Male",
                        expected_graduation=datetime(year=2019, month=1, day=1),
                        admission_date=datetime(year=2019, month=1, day=1),
                        parent_id=self.user.id, dob=datetime(year=2019, month=1, day=1),)
        parent = Parent(
            parent_id=self.user.id,
            marital_status="Married",
            occupation="Engineer",
            student_id=child.id
        )

        parent.students.append(child)
        parent.students.append(child)
        self.session.add(parent)
        self.session.commit()

        queried_parent = self.session.query(Parent).first()
        self.assertEqual(len(queried_parent.students), 1)
        self.assertEqual(queried_parent.students[0], child)

    def test_multiple_children(self):
        # Add multiple children to the parent and test if they are correctly associated
        child1 = Student(first_name="John", last_name="Doe", email="johndoe@localhost",
                         password="**HASHED_PASSWORD**",  # Use a secure hashing algorithm
                         other_names="Ametepe", gender="Male",
                         expected_graduation=datetime(year=2019, month=1, day=1),
                         admission_date=datetime(year=2019, month=1, day=1),
                         parent_id=self.user.id, dob=datetime(year=2019, month=1, day=1),)
        child2 = Student(first_name="Jane", last_name="Doe", email="janedoe@localhost",
                         password="**HASHED_PASSWORD**",  # Use a secure hashing algorithm
                         other_names="Ametepe", gender="Female",
                         expected_graduation=datetime(year=2019, month=1, day=1),
                         admission_date=datetime(year=2019, month=1, day=1),
                         parent_id=self.user.id,dob=datetime(year=2019, month=1, day=1),)

        parent = Parent(
            parent_id=self.user.id,
            marital_status="Married",
            occupation="Engineer"
        )

        parent.students.append(child1)
        parent.students.append(child2)
        self.session.add(parent)
        self.session.commit()

        queried_parent = self.session.query(Parent).first()
        self.assertEqual(len(queried_parent.students), 2)
        self.assertIn(child1, queried_parent.students)
        self.assertIn(child2, queried_parent.students)


if __name__ == '__main__':
    unittest.main()
