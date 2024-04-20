from os import environ

from models.announcement import Announcement
from models.attendance import Attendance
from models.basemodel import BaseModel
from models.classe import Class
from models.course import Course
from models.engine.dbstorage import DBStorage
from models.engine.filestorage import FileStorage
from models.feedbacks import Feedbacks
from models.gradebook import Gradebook
from models.parent import Parent
from models.permission import Permission
from models.staff import Staff
from models.student import Student
from models.user import User

STORAGE_ENGINE = environ.get('STORAGE_ENGINE', 'filesystem')

if STORAGE_ENGINE == 'filesystem':
    storage = FileStorage()
else:
    storage = DBStorage()
storage.reload()
