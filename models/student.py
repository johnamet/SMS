#!/usr/bin/python3
"""
Student Model
"""
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.orm import relationship, validates

from models.basemodel import Base, BaseModel
# from models.parent_child_assoc import ParentChildAssociation
from models.class_student_association import StudentClassAssociation


class Student(BaseModel, Base):
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
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    other_names = Column(String(50))
    dob = Column(Date, default=datetime.today)
    gender = Column(String(50), nullable=False)
    parent_id = Column(String(50), ForeignKey('parents.id'), nullable=False)
    attendances = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    expected_graduation = Column(Date, nullable=False, default=datetime.now())
    admission_date = Column(Date, nullable=False, default=datetime.now())
    class_ = relationship(StudentClassAssociation, back_populates="student")
    parents = relationship("Parent", back_populates="students")
    gradebooks = relationship("Grade",
                              back_populates='student',
                              cascade='all, delete')

    @validates('attendances')
    def validate_attendances(self, key, attendance):
        if not attendance:
            raise ValueError("A student must have at least one attendance record.")
        return attendance

    @validates("gender")
    def validate_gender(self, key, gender):
        if gender.lower() not in ["male", "female"]:
            raise ValueError("Gender must be either male or female")
        return gender

    def __init__(self,
                 first_name,
                 last_name,
                 gender,
                 parent_id,
                 expected_graduation: datetime,
                 admission_date: datetime,
                 dob=datetime.now(),
                 other_names=None, *args, **kwargs):
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
        self.first_name = first_name
        self.last_name = last_name
        self.other_names = other_names
        self.dob = dob
        self.gender = gender
        self.parent_id = parent_id
        self.expected_graduation = expected_graduation
        self.admission_date = admission_date
