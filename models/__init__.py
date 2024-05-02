from os import environ

from models.announcement import Announcement
from models.attendance import Attendance
from models.basemodel import BaseModel, Base
from models.class_course_assoc import ClassCourseAssociation
from models.class_student_association import StudentClassAssociation
from models.classe import Class
from models.course import Course
from models.engine.dbstorage import DBStorage
from models.engine.filestorage import FileStorage
from models.grade import Grade
from models.parent import Parent
from models.permission import Permission
from models.staff import Staff
from models.student import Student
from models.user import User

STORAGE_ENGINE = environ.get('STORAGE_ENGINE', 'db')

if STORAGE_ENGINE == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
