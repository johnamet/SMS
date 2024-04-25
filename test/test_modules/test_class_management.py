#!/usr/bin/python3
"""
Tests for class management
"""
import unittest
from datetime import datetime
from faker import Faker
import random

from models import Class, Student, User, Staff, Parent, Course, storage
from modules.class_management.class_management import ClassManagement
from modules.test_utils import populate_db


class ClassManagementTestCase(unittest.TestCase):
    def setUp(self):
        self.class_management = ClassManagement()
        self.faker = Faker()
        self.user = User(first_name=self.faker.first_name(), last_name=self.faker.last_name(),
                         email=self.faker.email(), password=self.faker.password(),
                         is_staff=True, is_active=True, gender=random.choice(['male', 'female']))

        self.user1 = User(first_name=self.faker.first_name(), last_name=self.faker.last_name(),
                          email=self.faker.email(), password=self.faker.password(),
                          is_staff=True, is_active=True, gender=random.choice(['male', 'female']))
        self.user.save()
        self.user1.save()

        self.user2 = User(first_name=self.faker.first_name(), last_name=self.faker.last_name(),
                          email=self.faker.email(), password=self.faker.password(),
                          is_staff=True, is_active=True, gender=random.choice(['male', 'female']))

        self.user2.save()

        self.parent = Parent(self.user2.id)

    def tearDown(self):
        self.class_management = None

    def _create_students(self, parent_id, range_=50):
        students = []
        for _ in range(range_):
            student = Student(first_name=self.faker.first_name(), last_name=self.faker.last_name(),
                              dob=self.faker.date_between(start_date='-25y', end_date='-25y'),
                              parent_id=parent_id,
                              expected_graduation=self.faker.date_time(),
                              gender=random.choice(["Male", "Female"]),
                              admission_date=datetime.now())
            student.save()
            students.append(student)
        return students

    def _create_staff_member(self):
        staff = Staff(id=self.user.id)
        staff.save()
        parent = Parent(parent_id=self.user1.id)
        parent.save()
        return staff, parent

    def _create_class(self):
        head_teacher, _ = self._create_staff_member()
        new_class = Class(class_name="Class 1", head_class_teacher=head_teacher.id, academic_year="2023/24")
        new_class.save()
        return new_class

    def test_enroll_student(self):
        new_class = self._create_class()
        parent = Parent(parent_id=self.user1.id)
        students = self._create_students(parent.id)

        # Test student enrollment
        for student in students:
            if storage.get_by_id(Student, student.id):
                (enrol, msg) = self.class_management.enroll_student(new_class.id, student.id)

        fetched_class = storage.get_by_id(Class, new_class.id)
        fetched_students = fetched_class.students

        self.assertEqual(len(fetched_students), 50)

    def test_get_unenroll(self):
        new_class = self._create_class()
        parent = Parent(parent_id=self.user1.id)
        student = self._create_students(parent.id, 1)[0]

        fetch_student = storage.get_by_id(Student, student.id)

        self.assertIsNotNone(fetch_student)
        self.assertIsInstance(fetch_student, Student)

        unenroll = self.class_management.unenroll_student(class_id=new_class.id,
                                                          student_id=fetch_student.id)
        self.assertTrue(unenroll)

    def test_create_class(self):
        course = Course(
            course_name="Mathematics",
            course_description="Introduction to Algebra",
            teacher_id=self.user.id
        )

        staff, _ = self._create_staff_member()

        course.save()
        new_class = self.class_management.create_class(class_name="Class 1",
                                                       head_class_teacher=staff.id,
                                                       academic_year="2023/24", courses_list=[course])
        self.assertTrue(new_class)

    def test_get_class(self):
        new_class = self._create_class()

        fetched_class = self.class_management.get_class(class_id=new_class.id)

        self.assertIsNotNone(fetched_class)

    def test_get_class_details(self):
        class_id = populate_db()

        result, msg = self.class_management.get_class_details(class_id=class_id)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
