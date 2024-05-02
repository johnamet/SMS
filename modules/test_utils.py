import random
from datetime import datetime

from faker import Faker

from models import User, Staff, Parent, Class, Student, Attendance, Course, Grade, StudentClassAssociation
from modules.class_management.class_management import ClassManagement

faker = Faker()

term = random.choice(["Term 1", "Term 2", "Term 3"])
academic_year = random.choice(["2023/24", "2024/25", ])
status = random.choice([1, 0])
desc = random.choice(["Homework", "Classwork", "Assessment", "Exam", "ClassTest", "quiz", "dictation"])
grade = random.choice(list(range(0, 11)))
class_management = ClassManagement()


def create_staff_member():
    user = User(first_name=faker.first_name(), last_name=faker.last_name(),
                email=faker.email(), password="StrongPassword!",
                is_staff=True, is_active=True, gender=random.choice(['male', 'female']))
    user.save()
    staff = Staff(id=user.id)
    staff.save()
    parent = Parent(parent_id=user.id)
    parent.save()
    return staff, parent


def create_attendance(student_id, class_id):
    attendance = Attendance(student_id=student_id,
                            class_id=class_id, term=term,
                            academic_year=academic_year, status=status)

    attendance.save()


def create_course(class_id, staff_id):
    course_dict = {
        "course_name": "Test Course",
        "course_description": "This is a test course",
        "teacher_id": staff_id,
        "class_id": class_id,
    }

    course = Course(**course_dict)
    course.save()

    return course


def create_grade(student_id, class_id, course_id):
    grade_ = Grade(student_id=student_id, class_id=class_id, course_id=course_id,
                   grade=grade, out_of=10, grade_desc=desc, term=term, academic_year=academic_year)

    grade_.save()


def create_class():
    head_teacher, _ = create_staff_member()
    new_class = Class(class_name="Class 1", head_class_teacher=head_teacher.id, academic_year="2023/24")
    new_class.save()
    return new_class


def create_students(parent_id, range_=50):
    students = []
    for _ in range(range_):
        student = Student(first_name=faker.first_name(), last_name=faker.last_name(),
                          dob=faker.date_between(start_date='-25y', end_date='-25y'),
                          parent_id=parent_id,
                          expected_graduation=faker.date_time(),
                          gender=random.choice(["Male", "Female"]),
                          admission_date=datetime.now())
        students.append(student)
        student.save()
    return students


def populate_db(range_=50):
    class_ = create_class()
    staff, parent = create_staff_member()
    students = create_students(parent.id, range_)
    course = create_course(class_.id, staff.id)
    for student in students:
        asoc = StudentClassAssociation(student_id=student.id, class_id=class_.id)
        asoc.save()
        # class_management.enroll_student(class_id=class_.id, student_id=student.id)
        for _ in range(10):
            create_attendance(student.id, class_.id)

        for _ in range(20):
            create_grade(student.id, class_.id, course.id)

    return class_.id
