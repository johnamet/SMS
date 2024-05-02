#!/usr/bin/python3
"""
This module contains the Staff model.
"""

from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship, validates

from models.basemodel import BaseModel, Base
from models.qualification import Qualification


# Association table for the many-to-many relationship between Staff and Course
staff_course_association = Table('staff_course_association', Base.metadata,
                                 Column('staff_id', String(50), ForeignKey('staff.id')),
                                 Column('course_id', String(50), ForeignKey('courses.id'))
                                 )



class Staff(BaseModel, Base):
    """
    Staff model represents the staff members of the institution.

    Args:
        id (str): The ID of the staff member, linked to a user in the database.
        marital_status (str): The marital status of the staff member.
        qualifications (list): The qualifications of the staff member.
        bank_acc (str): The bank account of the staff member.
        department (str): The department of the staff member.
        pension_fund_acc (str): The pension fund account of the staff member.
        role (str): The role of the staff member.
        status (str): The status of the staff member.
        courses (list): The courses of the staff member.

    Attributes:
        id (str): The ID of the staff member, linked to a user in the database.
        marital_status (str): The marital status of the staff member.
        qualifications (list): The qualifications of the staff member.
        bank_acc (str): The bank account of the staff member.
        department (str): The department of the staff member.
        pension_fund_acc (str): The pension fund account of the staff member.
        status (str): The status of the staff member.
        role (str): The role of the staff member.
        courses (list): The courses of the staff member.
    """

    __tablename__ = 'staff'

    id = Column(String(50), ForeignKey("users.id"), primary_key=True)
    marital_status = Column(String(50), nullable=True)
    bank_acc = Column(String(50), nullable=True)
    department = Column(String(50), nullable=True)
    pension_fund_acc = Column(String(50), nullable=True)
    role = Column(String(50), nullable=True)
    status = Column(String(50), nullable=True)
    qualifications = relationship("Qualification", backref="staff")
    courses = relationship("Course", secondary=staff_course_association, backref="staff")

    @validates('marital_status')
    def validate_marital_status(self, key, marital_status):
        if marital_status is not None and (marital_status.lower() not in ['single', 'married', 'divorced', 'widowed']):
            raise ValueError("Invalid marital status. Must be one of: Single, Married, Divorced, Widowed")
        return marital_status

    @validates('bank_acc', 'pension_fund_acc')
    def validate_bank_pension_acc(self, key, acc):
        if acc is not None and (not acc.isdigit() or len(acc) != 10):
            raise ValueError("Invalid account number. Must be a 10-digit number.")
        return acc

    def __init__(self, id, marital_status=None, qualifications=[], bank_acc=None,
                 department=None, pension_fund_acc=None, role="teacher", status="active",
                 *args, **kwargs):
        """
        Initialize a Staff instance.

        Args:
            id (str): The ID of the staff member, linked to a user in the database.
            marital_status (str): The marital status of the staff member.
            qualifications (list): The qualifications of the staff member.
            bank_acc (str): The bank account of the staff member.
            department (str): The department of the staff member.
            pension_fund_acc (str): The pension fund account of the staff member.
            role (str): The role of the staff member.
            status (str): The status of the staff member.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self.id = id
        self.marital_status = marital_status
        self.bank_acc = bank_acc
        self.department = department
        self.pension_fund_acc = pension_fund_acc
        self.status = status
        self.role = role
        self.qualification = qualifications
