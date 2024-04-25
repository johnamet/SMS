import unittest
from datetime import datetime
from faker import Faker
import random

from models import Attendance, storage, Staff, Class, Student, User, Parent
from modules import AttendanceManagement


class TestAttendanceManagement(unittest.TestCase):

    def setUp(self):
        self.attendance_management = AttendanceManagement(class_id="12453", term="Term 2", academic_year="2022/23")
        self.faker = Faker()

    def _create_staff_member(self):
        self.user = User(first_name=self.faker.first_name(), last_name=self.faker.last_name(),
                    email=self.faker.email(), password=self.faker.password(),
                    is_staff=True, is_active=True, gender=random.choice(['male', 'female']))
        self.user.save()
        staff = Staff(id=self.user.id)
        staff.save()
        parent = Parent(parent_id=self.user.id)
        parent.save()
        return staff, parent

    def _create_class(self):
        head_teacher, _ = self._create_staff_member()
        new_class = Class(class_name="Class 1", head_class_teacher=head_teacher.id, academic_year="2023/24")
        new_class.save()
        return new_class

    def _create_students(self, class_id, parent_id):
        students = []
        for _ in range(50):
            student = Student(first_name=self.faker.first_name(), last_name=self.faker.last_name(),
                              dob=self.faker.date_between(start_date='-25y', end_date='-25y'),
                              class_id=class_id, parent_id=parent_id,
                              expected_graduation=self.faker.date_time(),
                              gender=random.choice(["Male", "Female"]),
                              admission_date=datetime.now())
            students.append(student)
            student.save()
        return students

    def test_create_attendance_record(self):
        new_class = self._create_class()
        self.attendance_management.class_id = new_class.id
        parent = Parent(parent_id=self.user.id)
        students = self._create_students(new_class.id, parent.id)
        attendance = self.attendance_management.create_attendance(student_id=students[0].id, status=1)
        self.assertIsInstance(attendance, Attendance)
        fetched_attendance = storage.get_by_id(Attendance, attendance.id)
        self.assertIsNotNone(fetched_attendance)

    def test_mark_attendance(self):
        new_class = self._create_class()
        self.attendance_management.class_id = new_class.id
        parent = Parent(parent_id=self.user.id)
        students = self._create_students(new_class.id, parent.id)
        attendances = []
        for _ in range(100):
            attendances.append(Attendance(student_id=random.choice([student.id for student in students]),
                                          class_id=new_class.id,
                                          date=self.faker.date_time_between(datetime(2023, 1, 1),
                                                                            datetime(2025, 1, 2)),
                                          academic_year=random.choice(["2023/24", "2024/25"]),
                                          term=random.choice(["Term 1", "Term 2", "Term 3"]),
                                          status=random.choice([1, 0])))
        self.attendance_management.mark_attendance(attendances)
        fetched_attendance = storage.get_by_id(Attendance, attendances[0].id)
        self.assertIsNotNone(fetched_attendance)
        fetched_attendances = storage.all(Attendance)
        self.assertEqual(len(fetched_attendances), 201)

    def test_get_attendance_records(self):
        new_class = self._create_class()
        self.attendance_management.class_id = new_class.id
        parent = Parent(parent_id=self.user.id)
        students = self._create_students(new_class.id, parent.id)
        attendances = []
        for _ in range(100):
            attendances.append(Attendance(student_id=random.choice([student.id for student in students]),
                                          class_id=new_class.id,
                                          date=self.faker.date_time_between(datetime(2023, 1, 1),
                                                                            datetime(2025, 1, 2)),
                                          academic_year=random.choice(["2023/24", "2024/25"]),
                                          term=random.choice(["Term 1", "Term 2", "Term 3"]),
                                          status=random.choice([1, 0])))
        self.attendance_management.mark_attendance(attendances)
        fetched_attendances = storage.all(Attendance)
        self.assertEqual(len(fetched_attendances.values()), 101)
        class_attendance = self.attendance_management.get_attendance_by_class_id(new_class.id)
        self.assertIsInstance(class_attendance[0], Attendance)
        student_attendance = self.attendance_management.get_student_attendance(random.choice(students).id)
        self.assertIsNotNone(student_attendance)

    def test_update_attendance_record(self):
        new_class = self._create_class()
        self.attendance_management.class_id = new_class.id
        parent = Parent(parent_id=self.user.id)
        students = self._create_students(new_class.id, parent.id)
        attendance = self.attendance_management.create_attendance(student_id=students[0].id, status=1)
        fetched_attendance = storage.get_by_id(Attendance, attendance.id)
        self.assertIsNotNone(fetched_attendance)
        result = self.attendance_management.update_attendance(fetched_attendance.id, **{"term": "Term2"})
        self.assertTrue(result)

    def test_error_handling(self):
        with self.assertRaises(ValueError):
            self.attendance_management.class_id = None
            self.attendance_management.create_attendance(student_id="1234", status=1)


if __name__ == "__main__":
    unittest.main()
