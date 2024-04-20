#!/usr/bin/python
"""
The script defines the class Course
"""
from sqlalchemy import Column, String, ForeignKey

from models.basemodel import BaseModel, Base


class Course(BaseModel, Base):
    """
    The class defines the class Course
    """
    __tablename__ = 'courses'
    course_name = Column(String, nullable=False)
    course_description = Column(String, nullable=False)
    teacher_id = Column(String, ForeignKey("staff.id"), nullable=False)


    def __init__(self,
                 course_name,
                 course_description,
                 teacher_id, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self.course_name = course_name
        self.course_description = course_description
        self.teacher_id = teacher_id
