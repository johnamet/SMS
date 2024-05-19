import random
from datetime import datetime, timedelta, date
from faker import Faker
from models import User, Staff, Parent, Class, Student, Attendance, Course, Grade, StudentClassAssociation, storage, \
    ClassCourseAssociation
from modules.class_management.class_management import ClassManagement

faker = Faker()

TERMS = ["Term 1", "Term 2", "Term 3"]
ACADEMIC_YEARS = ["2023/24", "2024/25", "2025/26", "2026/27", "2027/28"]
SUBJECTS = ["Mathematics", "Religious & Moral Education", "Pre-Technical Education", "Home Economics",
            "English Language", "Social Studies"]
DESCRIPTIONS = ["Homework", "Classwork", "Assessment", "Exam", "ClassTest", "quiz", "dictation"]
CLASSES = ["Basic 1", "Basic 2", "Basic 3", "Basic 4", "Basic 5", "Basic 6", "Basic 7"]
class_label = ["A", "B", "C", "D", "E", "F"]

class_management = ClassManagement()


def create_staff_member():
    """Create a staff member and associated parent."""
    first_name = faker.first_name()
    last_name = faker.last_name()
    email = faker.email()
    user = User(first_name=first_name, last_name=last_name, email=email, password="StrongPassword!1234",
                is_staff=True, is_active=True, gender=random.choice(['male', 'female']))
    user.save()
    staff = Staff(id=user.id)
    staff.save()
    parent = Parent(parent_id=user.id)
    parent.save()
    return staff, parent


# Define start and end dates for your desired range
start_date = date(2023, 1, 1)  # Replace with your desired start date
end_date = date(2024, 5, 13)  # Replace with your desired end date (today's date is 2024-05-12)

# Generate a random date between the start and end dates
time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days
random_number_of_days = random.randrange(days_between_dates)
random_date = start_date + timedelta(days=random_number_of_days)


def create_attendance(student_id, class_id):
    """Create attendance record for a student in a class."""
    attendance = Attendance(student_id=student_id, class_id=class_id, term=random.choice(TERMS),
                            date=faker.date_between(start_date, end_date), academic_year=random.choice(ACADEMIC_YEARS),
                            status=random.choice([1, 0]))
    attendance.save()


def create_course(class_id, staff_id, classes):
    """Create a course for a class taught by a staff member."""
    course_dict = {
        "course_name": random.choice(SUBJECTS),
        "course_description": "This is a test course",
        "teacher_id": staff_id,
        "class_id": class_id,
        "department": random.choice(["Primary Department", "Secondary Department"]),
    }

    course = Course(**course_dict)
    for class_ in classes:
        association = ClassCourseAssociation(classe=class_)
        course.classes.append(association)
    course.save()
    return course


def create_grade(student_id, class_id, course_id):
    """Create a grade for a student in a class."""
    grade = Grade(student_id=student_id, class_id=class_id, course_id=course_id,
                  grade=random.choice(range(0, 11)), out_of=10, grade_desc=random.choice(DESCRIPTIONS),
                  term=random.choice(TERMS), academic_year=random.choice(ACADEMIC_YEARS))
    grade.save()
    return grade.id


def create_class(name, staff_id, students, assist_clss_teacher_id):
    """Create a class with a head teacher and enrolled students."""
    new_class = Class(class_name=name, head_class_teacher=staff_id,
                      academic_year=random.choice(ACADEMIC_YEARS),
                      assist_class_teacher=assist_clss_teacher_id)
    for student in students:
        association = StudentClassAssociation(student=student)
        new_class.students.append(association)
    new_class.save()
    return new_class


def create_students(parent_id, range_=50):
    """Create a specified number of students associated with a parent."""
    students = []
    for _ in range(range_):
        student = Student(first_name=faker.first_name(), last_name=faker.last_name(),
                          dob=faker.date_between(start_date='-25y', end_date='-25y'),
                          parent_id=parent_id, expected_graduation=faker.date_time(),
                          gender=random.choice(["Male", "Female"]), admission_date=datetime.now())
        student.save()
        storage.save()
        students.append(student)
    return students


def populate_db(range_=50):
    """Populate the database with staff, parents, students, classes, courses, grades, and attendance records."""
    parents = []
    teachers = []
    for _ in range(range_):
        teacher, parent = create_staff_member()
        parents.append(parent.id)
        teachers.append(teacher.id)

    classes = []
    students = create_students(random.choice(parents))
    for _ in range(range_):
        new_class = create_class(random.choice(CLASSES) + random.choice(class_label),
                                 random.choice(teachers), students,
                                 random.choice(teachers))
        classes.append(new_class)

    courses = []
    for _ in range(range_):
        course = create_course(random.choice(classes), random.choice(teachers), classes)
        courses.append(course.id)

    grades = []
    for _ in range(range_):
        grade_id = create_grade(random.choice([student.id for student in students]),
                                random.choice([class_.id for class_ in classes]),
                                random.choice(courses))
        grades.append(grade_id)

    for student in students:
        for _ in range(range_):
            create_attendance(student.id, random.choice([class_.id for class_ in classes]))



if __name__ == '__main__':
    populate_db()
