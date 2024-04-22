#!/usr/bin/python3
"""
Student Model
"""
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship, validates

from models.basemodel import Base
from models.gradebook import Gradebook
from models.attendance import Attendance
from models.user import User
# from models.parent_child_assoc import ParentChildAssociation


class Student(User, Base):
    """
    Student Model represents a student in the system.

    Args:
        parent_id (str): The ID of the parent student.
        expected_graduation (datetime): The expected graduation date of the student.
        admission_date (datetime): The admission date of the student.

    Attributes:
        parent_id (str): The ID of the parent student.
        expected_graduation (datetime): The expected graduation date of the student.
        admission_date (datetime): The admission date of the student.
        parents (relationship): Relationship attribute to access the associated parent(s).
        gradebooks (relationship): Relationship attribute to access the associated gradebooks.
    """

    __tablename__ = 'students'
    id = Column(String(50), ForeignKey('users.id'), primary_key=True)
    parent_id = Column(String(50), ForeignKey('parents.id'), nullable=False)
    attendances = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    expected_graduation = Column(Date, nullable=False, default=datetime.now())
    admission_date = Column(Date, nullable=False, default=datetime.now())
    # parents = relationship("Parent", back_populates="students", cascade="all, delete-orphan")
    gradebooks = relationship(Gradebook,
                              back_populates='student',
                              cascade='all, delete')

    @validates('attendances')
    def validate_attendances(self, key, attendance):
        if not attendance:
            raise ValueError("A student must have at least one attendance record.")
        return attendance

    def __init__(self, parent_id, expected_graduation: datetime, admission_date: datetime, *args, **kwargs):
        """
        Initialize a Student instance.

        Args:
            parent_id (str): The ID of the parent student.
            expected_graduation (datetime): The expected graduation date of the student.
            admission_date (datetime): The admission date of the student.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.parent_id = parent_id
        self.expected_graduation = expected_graduation
        self.admission_date = admission_date
