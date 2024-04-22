import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.basemodel import Base
from models.course import Course


class TestCourseModel(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)
        self.course = Course(
            course_name="Mathematics",
            course_description="Introduction to Algebra",
            teacher_id="12345"
        )
        self.session.add(self.course)
        self.session.commit()

    def tearDown(self):
        self.session.rollback()

    def test_create_course(self):
        retrieved_course = self.session.query(Course).filter_by(course_name="Mathematics").first()
        self.assertIsNotNone(retrieved_course)
        self.assertEqual(retrieved_course.course_name, "Mathematics")
        self.assertEqual(retrieved_course.course_description, "Introduction to Algebra")
        self.assertEqual(retrieved_course.teacher_id, "12345")

    def test_update_course(self):
        self.course.update(course_description="Advanced Algebra")
        self.session.commit()
        retrieved_course = self.session.query(Course).filter_by(course_name="Mathematics").first()
        self.assertEqual(retrieved_course.course_description, "Advanced Algebra")
        self.assertTrue(retrieved_course.updated_at > retrieved_course.created_at)

    def test_course(self):
        self.assertTrue(self.course is not None)

    def test_course_name(self):
        self.assertEqual(self.course.course_name, "Mathematics")

    def test_delete_course(self):
        self.session.delete(self.course)
        self.session.commit()
        retrieved_course = self.session.query(Course).filter_by(course_name="Mathematics").first()
        self.assertIsNone(retrieved_course)

    def test_course_created_at(self):
        self.assertTrue(isinstance(self.course.created_at, datetime))

    def test_course_updated_at(self):
        self.assertTrue(isinstance(self.course.updated_at, datetime))

    def test_course_description(self):
        self.assertEqual(self.course.course_description, "Introduction to Algebra")

    def test_teacher_id(self):
        self.assertEqual(self.course.teacher_id, "12345")

    def test_created_at(self):
        self.assertTrue(self.course.created_at < datetime.now())

    def test_updated_at(self):
        self.assertTrue(self.course.updated_at < datetime.now())

    def test_update(self):
        self.course.update(course_description="Advanced Algebra")
        self.assertEqual(self.course.course_description, "Advanced Algebra")
        self.assertTrue(self.course.updated_at > self.course.created_at)


if __name__ == '__main__':
    unittest.main()
