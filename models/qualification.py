#!/usr/bin/python3
"""
Qualification Model
"""

from sqlalchemy import Column, String, ForeignKey

from models.basemodel import Base, BaseModel


class Qualification(BaseModel, Base):
    """
    Qualification Model: the qualifications of staff
    Args:
        name (str): Qualification name
        staff_id (str): Staff ID of the staff with the qualification
    """
    __tablename__ = 'qualifications'
    name = Column(String, nullable=False)
    staff_id = Column(String, ForeignKey("staff.id"), nullable=False)

    def __init__(self, name, staff_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.staff_id = staff_id