#!/usr/bin/python3
import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Parent, Grade, Attendance, Staff, Class
from models.student import Student
from models.class_student_association import StudentClassAssociation


class TestStudentRelationships(unittest.TestCase):
    def setUp(self):
        # Set up an in-memory SQLite database for testing
        engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

        # Create sample data for testing relationships
        self.parent = Parent(parent_id="parent_1")
        self.student = Student(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="password",
            gender="Male",
            parent_id="parent_1",
            dob=datetime(1995, 1, 2),
            expected_graduation=datetime(2026, 6, 30),
            admission_date=datetime(2021, 9, 1)
        )

        # Create staff members
        head_teacher = Staff(id="1", first_name="John", last_name="Doe", email="john.doe@example.com")
        assistant_teacher = Staff(id="2", first_name="Jane", last_name="Smith", email="jane.smith@example.com")

        # Create a class
        self.class1 = Class(class_name="Class 1", head_class_teacher=head_teacher.id, academic_year="2022/23",
                       assist_class_teacher=assistant_teacher.id)
        self.class2 = Class(class_name="Class 2", head_class_teacher=head_teacher.id, academic_year="2023/24",
                       assist_class_teacher=assistant_teacher.id)

        self.parent.students.append(self.student)

        self.gradebook1 = Grade(course_id="course_1", student_id=self.student.id, grade=15, class_id="class_id",
                                grade_desc="homework", term="Term 2", academic_year="2023/24")
        self.gradebook2 = Grade(course_id="course_2", student_id=self.student.id, grade=15, class_id="class_id",
                                grade_desc="homework", term="Term 2",academic_year="2023/24")
        self.attendance1 = Attendance(date=datetime(2024, 4, 20), student_id=self.student.id,
                                      class_id="class_id", term="Term 2", status=1, academic_year="2022/2023")
        self.attendance2 = Attendance(date=datetime(2024, 4, 21), student_id=self.student.id,
                                      class_id="class_id", term="Term 2", status=1, academic_year="2022/2023")

        a = StudentClassAssociation()
        a1 = StudentClassAssociation()
        a.student = self.student
        a1.student = self.student

        self.class2.students.append(a)
        self.class1.students.append(a1)
        # self.class2.students.append(self.student)

        self.session.add_all([self.parent, self.student, self.gradebook1, self.gradebook2,
                              self.attendance1, self.attendance2, self.class2, self.class1, head_teacher,
                              assistant_teacher])

        self.session.commit()

    def test_student_parent_relationship(self):
        queried_student = self.session.query(Student).filter_by(id=self.student.id).first()
        self.assertEqual(queried_student.parent_id, self.parent.id)
        self.assertEqual(queried_student.parents, self.parent)

    def test_student_gradebooks_relationship(self):
        queried_student = self.session.query(Student).filter_by(id=self.student.id).first()
        self.assertEqual(len(queried_student.gradebooks), 2)
        self.assertIn(self.gradebook1, queried_student.gradebooks)
        self.assertIn(self.gradebook2, queried_student.gradebooks)

    def test_student_attendances_relationship(self):
        queried_student = self.session.query(Student).filter_by(id=self.student.id).first()
        self.assertEqual(len(queried_student.attendances), 2)
        self.assertIn(self.attendance1, queried_student.attendances)
        self.assertIn(self.attendance2, queried_student.attendances)

    def test_student_classes_relationship(self):
        queried_class = self.session.query(Class).filter_by(class_name="Class 1").first()
        queried_class2 = self.session.query(Class).filter_by(class_name="Class 2").first()
        self.assertEqual(len(queried_class.students), 1)
        self.assertEqual(len(queried_class2.students), 1)

        queried_student = self.session.query(Student).filter_by(id=self.student.id).first()
        self.assertEqual(len(queried_student.class_), 2)
        self.assertIsInstance(queried_class2.students, list)

    def test_student(self):
        self.assertTrue(self.student is not None)

    def test_first_name(self):
        self.assertEqual(self.student.first_name, "John")

    def test_last_name(self):
        self.assertEqual(self.student.last_name, "Doe")

    def test_email(self):
        self.assertEqual(self.student.email, "john@example.com")

    def test_parent_id(self):
        self.assertEqual(self.student.parent_id, "parent_1")

    def test_expected_graduation(self):
        self.assertEqual(self.student.expected_graduation, datetime(2026, 6, 30).date())

    def test_admission_date(self):
        self.assertEqual(self.student.admission_date, datetime(2021, 9, 1).date())

    def test_created_at(self):
        self.assertTrue(self.student.created_at < datetime.now())

    def test_updated_at(self):
        self.assertTrue(self.student.updated_at < datetime.now())

    def test_update(self):
        self.student.update(expected_graduation=datetime(2027, 6, 30))
        self.assertEqual(self.student.expected_graduation, datetime(2027, 6, 30))
        self.assertTrue(self.student.updated_at > self.student.created_at)


if __name__ == '__main__':
    unittest.main()
