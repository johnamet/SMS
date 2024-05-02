#!/usr/bin/python3


import random
from datetime import datetime

from faker import Faker

from models import User, Staff, Class, Parent, Student
from models.attendance import Attendance

faker = Faker()

user = User(first_name=faker.first_name(), last_name=faker.last_name(),
            email=faker.email(),
            password=faker.password(),
            is_staff=True,
            is_active=True, gender=random.choice(['male', 'female']))
user.save()
head_teacher = Staff(id=user.id, )
head_teacher.save()

# Create a class
new_class = Class(class_name="Class 1", head_class_teacher=head_teacher.id, academic_year="2023/24")
new_class.save()

parent = Parent(parent_id=user.id)
parent.save()

student = Student(first_name=faker.first_name(), last_name=faker.last_name(),
                  email=faker.email(), class_id=new_class.id, parent_id=parent.id,
                  expected_graduation=faker.date_time(),
                  gender=random.choice(["Male", "Female"]),
                  admission_date=datetime.now())

student.save()

attendance = Attendance(student_id=student.id,
                        class_id=new_class.id,
                        date=faker.date_time_between(datetime(2023, 1, 1),
                                                     datetime(2025, 1, 2)),
                        academic_year=random.choice(["2023/24", "2024/25"]),
                        term=random.choice(["Term 1", "Term 2", "Term 3"]),
                        status=random.choice([1, 0]))

attendance.save()
