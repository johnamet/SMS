#!/usr/bin/python3

"""
The script defines the attendance model
"""
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

    def __init__(self, class_id, student_id, term, status, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.class_id = class_id
        self.student_id = student_id
        self.term = term
        self.status = status