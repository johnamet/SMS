#!/usr/bin/python3

"""
This module contains the Attendance model
"""
import datetime

from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Date
from sqlalchemy.orm import relationship

from models.basemodel import BaseModel, Base


class Attendance(BaseModel, Base):
    """
    The Attendance model represents the attendance of students in classes.

    Args:
        class_id (str): The ID of the class where the attendance was recorded.
        student_id (str): The ID of the student whose attendance is recorded.
        term (str): The term or session during which the attendance was taken.
        status (int): The attendance status (1 for present, 0 for absent).

    Attributes:
        class_id (str): The ID of the class where the attendance was recorded.
        student_id (str): The ID of the student whose attendance is recorded.
        term (str): The term or session during which the attendance was taken.
        status (int): The attendance status (1 for present, 0 for absent).
        date (datetime): The date and time when the attendance was taken.
        classe (relationship): Relationship attribute to access the related Class instance.
    """

    __tablename__ = 'attendance'
    class_id = Column(String(50), ForeignKey('classes.id'), nullable=False)
    student_id = Column(String(50), ForeignKey('students.id'), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    student = relationship("Student", back_populates="attendances")
    classe = relationship("Class", back_populates="attendances")
    academic_year = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False)
    term = Column(String(50), nullable=False)

    def __init__(self, class_id, student_id,
                 term, status,
                 date=datetime.datetime.now(),
                 *args, **kwargs):
        """
        Initialize an Attendance instance.

        Args:
            class_id (str): The ID of the class where the attendance was recorded.
            student_id (str): The ID of the student whose attendance is recorded.
            term (str): The term or session during which the attendance was taken.
            status (int): The attendance status (1 for present, 0 for absent).
            date (DateTime): The date the attendance was taken.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.class_id = class_id
        self.student_id = student_id
        self.term = term.strip()  # Remove leading/trailing whitespaces
        self.status = status
        self.date = date
