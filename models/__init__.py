from models.basemodel import BaseModel
from models.course import Course
from models.announcement import Announcement
from models.attendance import Attendance
from models.feedbacks import Feedbacks
from models.user import User
from models.gradebook import Gradebook
from models.permission import Permission
from models.staff import Staff
from models.parent import Parent
from models.student import Student


classes = {"BaseModel": BaseModel, "User": User,
           "Course": Course, "Announcement": Announcement,}