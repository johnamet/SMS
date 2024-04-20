#!/usr/bin/python3
"""
Student Model
"""
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from models import User
from models.basemodel import Base

class Student(User, Base):
    """
    Student Model
    Args:
        parent_id (str): Parent student id
        expected_graduation (datetime): Expected graduation date
        admission_date (datetime): Admission date
    """

    __tablename__ = 'students'
    parent_id = Column(String, ForeignKey('students.id'), nullable=False)
    expected_graduation = Column(DateTime, nullable=False)
    admission_date = Column(DateTime, nullable=False)
    parents = relationship('ParentChildAssociation', backref='student', cascade='all, delete')

    def __init__(self, parent_id,
                 expected_graduation,
                 admission_date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_id = parent_id
        self.expected_graduation = expected_graduation
        self.admission_date = admission_date
