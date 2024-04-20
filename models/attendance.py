#!/usr/bin/python3

"""
The script defines the attendance model
"""
from sqlalchemy import Column, String, ForeignKey, Integer

from models.basemodel import BaseModel


class Attendance(BaseModel):
    """
    The attendance model
    Args:
        class_id (str): The class id of the class
        student_id (str): The student id of the class
        status (int): 1 if present otherwise 0
    """

    __tablename__ = 'attendance'
    class_id = Column(String, ForeignKey('classes.id'), nullable=False)
    student_id = Column(String, ForeignKey('students.id'), nullable=False)
    status = Column(Integer, nullable=False)
    term = Column(String, nullable=False)

    def __init__(self, class_id, student_id, term, status, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_id = class_id
        self.student_id = student_id
        self.term = term
        self.status = status
