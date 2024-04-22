import json
import os

from models.feedback import Feedback

from models.announcement import Announcement
from models.attendance import Attendance
from models.basemodel import BaseModel
from models.classe import Class
from models.course import Course
from models.gradebook import Gradebook
from models.parent import Parent
from models.permission import Permission
from models.staff import Staff
from models.student import Student
from models.user import User

classes = {"BaseModel": BaseModel, "User": User,
           "Course": Course, "Announcement": Announcement,
           "Feedbacks": Feedback, "Student": Student, "Parent": Parent,
           "Staff": Staff, "Gradebook": Gradebook, "Permission": Permission,
           "Attendance": Attendance, "Class": Class}


class FileStorage:
    """
    FileStorage class to handle file storage
    Args:
        __file_storage_path (str): path to file storage
        __storage (str): file storage file
    """

    __file_storage_path = "./.store/"
    __storage = os.path.join(__file_storage_path, "file.json")
    __objs = {}

    def __init__(self):
        if not os.path.isfile(self.__storage):
            try:
                os.makedirs(self.__file_storage_path)
            except FileExistsError:
                pass

    def all(self, cls=None):
        filtered_objs = {}
        if cls is not None:
            for key, cls in self.__objs.items():
                if cls[__class__] == cls:
                    filtered_objs[key] = cls
            return filtered_objs
        return self.__objs

    def new(self, obj):
        """
        Add a new obj to storage
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objs[key] = obj
        self.save()

    def __serialize(self):
        objs_s = {}
        for key, obj in self.__objs.items():
            objs_s[key] = obj.serialize()
        return objs_s

    def __deserialize(self, data):
        for key, obj_data in data.items():
            cls = classes[obj_data['__class__']]
            self.__objs[key] = cls(**obj_data)

    def save(self):
        serialized_obj = self.__serialize()
        with open(self.__storage, "w") as file:
            json.dump(serialized_obj, file)

    def reload(self):
        try:
            with open(self.__storage, "r") as file:
                data = json.load(file)
                self.__deserialize(data)
        except FileNotFoundError:
            pass

    def close(self):
        self.__objs.clear()

    def delete(self, obj):
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objs.pop(key, None)
        self.save()
