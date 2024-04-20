#!/usr/bin/python3
"""
Parent model
"""
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from models.basemodel import BaseModel, Base

class Parent(BaseModel, Base):
    """
    Parent model
    Args:
        parent_id (int): Parent ID
        marital_status (str): Marital status
        occupation (str): Occupation
    """

    __tablename__ = 'parents'
    id = Column(String, ForeignKey("users.id"), primary_key=True)
    marital_status = Column(String)
    occupation = Column(String)
    children = relationship("ParentChildAssociation", back_ref="parent")

    def __init__(self, parent_id, marital_status=None, occupation=None, **kwargs):
        super().__init__(self, **kwargs)
        self.id = parent_id
        self.marital_status = marital_status
        self.occupation = occupation
