#!/usr/bin/python3
"""
This module contains the Staff model.
"""
from sqlalchemy import Column, String, ForeignKey

from models.basemodel import BaseModel, Base


class Staff(BaseModel, Base):
    """
    Staff model.
    Args:
        BaseModel ([type]): [description]
        id (str) : is linked to a user in the database.
        qualifications (list): the qualifications of the staff.
        bank_acc (str): the bank account of the staff.
        department (str): the department of the staff.
        pension_fund_acc (str): the pension fund account of the staff.
        status (str): the status of the staff.
        role (str): the role of the staff.
    """

    __tablename__ = 'staff'
    id = Column(String, ForeignKey("users.id"), primary_key=True)

    def __init__(self, id, marital_status=None,
                 qualifications=[],
                 bank_acc=None,
                 department=None,
                 pension_fund_acc=None, role="teacher",status="active", *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self.id = id
        self.marital_status = marital_status
        self.qualifications = qualifications
        self.bank_acc = bank_acc
        self.department = department
        self.pension_fund_acc = pension_fund_acc
        self.status = status
        self.role = role
