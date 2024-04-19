#!/usr/bin/python
"""
The script defines the class Course
"""
from models.basemodel import BaseModel


class Course(BaseModel):
    """
    The class defines the class Course
    """
    __tablename__ = 'courses'

    def __init__(self,
                 course_name,
                 course_description,
                 teacher_id, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self.course_name = course_name
        self.course_description = course_description
        self.teacher_id = teacher_id
