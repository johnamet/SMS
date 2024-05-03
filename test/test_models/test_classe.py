#!/usr/bin/python3
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Class, Staff, ClassCourseAssociation, Base


class TestClassModel(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    def tearDown(self):
        self.session.rollback()

    def test_create_class(self):
        # Create a staff member
        head_teacher = Staff(id="1", first_name="John", last_name="Doe", email="john.doe@example.com")
        self.session.add(head_teacher)
        self.session.commit()

        # Create a class
        new_class = Class(class_name="Class 1", head_class_teacher=head_teacher.id, academic_year="2023/24")
        self.session.add(new_class)
        self.session.commit()

        # Retrieve the class from the database
        retrieved_class = self.session.query(Class).filter_by(class_name="Class 1").first()

        # Assert that the retrieved class matches the created class
        self.assertIsNotNone(retrieved_class)
        self.assertEqual(retrieved_class.class_name, "Class 1")
        self.assertEqual(retrieved_class.head_class_teacher, head_teacher.id)
        self.assertEqual(retrieved_class.academic_year, "2023/24")

    def test_class_relationships(self):
        # Create staff members
        head_teacher = Staff(id="1", first_name="John", last_name="Doe", email="john.doe@example.com")
        assistant_teacher = Staff(id="2", first_name="Jane", last_name="Smith", email="jane.smith@example.com")
        self.session.add_all([head_teacher, assistant_teacher])
        self.session.commit()

        # Create a class
        new_class = Class(class_name="Class 1", head_class_teacher=head_teacher.id, academic_year="2023/24",
                          assist_class_teacher=assistant_teacher.id)
        self.session.add(new_class)
        self.session.commit()

        # Create a course
        course = ClassCourseAssociation(classe=new_class, course_id="COURSE1", description="Mathematics")
        self.session.add(course)
        self.session.commit()

        # Retrieve the class from the database
        retrieved_class = self.session.query(Class).filter_by(class_name="Class 1").first()

        # Check relationships
        self.assertIsNotNone(retrieved_class)
        self.assertEqual(len(retrieved_class.courses), 1)
        self.assertEqual(retrieved_class.courses[0].course_id, "COURSE1")

    def test_class_validations(self):
        # Create a class without required fields
        with self.assertRaises(Exception):
            new_class = Class(head_class_teacher="1", academic_year="2023/24")
            self.session.add(new_class)
            self.session.commit()


if __name__ == '__main__':
    unittest.main()
