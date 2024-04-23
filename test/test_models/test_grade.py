#!/usr/bin/python3

import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Gradebook, Course, Class, Student, Base


# Import your Gradebook and other model classes here


class TestGradebookModel(unittest.TestCase):
    def setUp(self):
        # Set up an in-memory SQLite database for testing
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

        # Create sample data for testing
        self.course = Course(course_name="Mathematics", course_description="Introduction to Algebra",
                             teacher_id="12345")
        self.class_ = Class(class_name="B7B", head_class_teacher="1245", academic_year="2023/24")
        self.student = Student(first_name="John",
                               last_name="Doe",
                               email="johndoe@example.com",
                               password="password", parent_id="123456",
                               admission_date=datetime.today(),
                               gender="Male",
                               expected_graduation=datetime(2025, 1, 5))
        self.gradebook_entry = Gradebook(grade=85, grade_desc="Homework", term="Term 1", course_id=self.course.id,
                                         class_id=self.class_.id,
                                         student_id=self.student.id)
        gradebook_entry2 = Gradebook(grade=86, grade_desc="Classwork", term="Term 2", course_id=self.course.id,
                                     class_id=self.class_.id,
                                     student_id=self.student.id)

        # Add sample data to the session
        self.session.add_all([self.course, self.class_, self.student, self.gradebook_entry, gradebook_entry2])
        self.session.commit()

    def test_gradebook_instantiation(self):
        # Test Gradebook instantiation
        self.assertIsInstance(self.gradebook_entry, Gradebook)
        self.assertIsNotNone(self.gradebook_entry.id)

    def test_gradebook_data_validation(self):
        # Test data validation (grade range)
        with self.assertRaises(ValueError):
            Gradebook(grade=152,
                      grade_desc="Homework",
                      term="Term 1",
                      course_id=self.course.id,
                      class_id=self.class_.id,
                      student_id=self.student.id)

    def test_relationships(self):
        # Test relationships
        queried_gradebook_entry = self.session.query(Gradebook).first()
        self.assertEqual(queried_gradebook_entry.course, self.course)
        self.assertEqual(queried_gradebook_entry.classe, self.class_)
        self.assertEqual(queried_gradebook_entry.student, self.student)

        queried_student = self.session.query(Student).first()
        self.assertEqual(len(queried_student.gradebooks), 2)

    def test_update_grade(self):
        # Test updating the grade
        self.gradebook_entry.update(grade=90)
        self.assertEqual(self.gradebook_entry.grade, 90)

    def test_delete_gradebook_entry(self):
        # Test deleting a gradebook entry
        self.session.delete(self.gradebook_entry)
        self.session.commit()
        self.assertIsNone(self.session.query(Gradebook).filter(Gradebook.id == self.gradebook_entry.id).first())

    def tearDown(self):
        # Clean up the session after each test
        self.session.close()


if __name__ == '__main__':
    unittest.main()
