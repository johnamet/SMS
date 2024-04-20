#!/usr/bin/python3

"""
The script defines the Gradebook class, which represents a Gradebook.
"""
from sqlalchemy import Column, Integer, ForeignKey

from models.basemodel import BaseModel, Base


class Gradebook(BaseModel, Base):
    """
    The Gradebook class represents a Gradebook.
    Args:
        grade (int): The grade of the gradebook.
        class_id (str): The class of the gradebook.
        course_id (str): The course of the gradebook.
        student_id (str): The student of the gradebook.
    """
    __tablename__ = 'gradebook'
    grade = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)

    def __init__(self, grade, course_id, class_id, student_id, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.grade = grade
        self.course_id = course_id
        self.class_id = class_id
        self.student_id = student_id
